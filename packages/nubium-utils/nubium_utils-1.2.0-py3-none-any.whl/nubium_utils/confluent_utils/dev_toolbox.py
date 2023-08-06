import itertools
from time import sleep

from confluent_kafka.cimpl import KafkaException
from confluent_kafka.error import KafkaError
from confluent_kafka.admin import AdminClient, NewTopic
from fastavro.validation import validate
from unittest.mock import MagicMock
from nubium_utils import log_and_raise_error
from nubium_utils.confluent_utils import get_producers, produce_message, get_consumer, enqueue_auto_commits, shutdown_cleanup, handle_no_messages
from nubium_topic_configs.topics import primary_topics, internal_topics, changelog_topics
from nubium_topic_configs.clusters import cluster_topic_map
from nubium_utils.confluent_utils.confluent_runtime_vars import env_vars
from nubium_utils.confluent_utils.consumer_utils import consume_all_messages
from nubium_utils.custom_exceptions import NoMessageError, SignalRaise


class KafkaToolbox:
    """
    Helpful functions for interacting with Kafka (mainly RHOSAK).
    Allows you to interface with multiple clusters at once by default assuming they are defined via your environment
    variables NUBIUM_CLUSTER_{N}. Actions include:

    Topics (multiple): create, delete, list.

    Messages (multiple): produce, consume
    """

    def __init__(self, configs=None, auto_configure=True):
        self.admin_clients = {}
        self.producers = {}
        self.consumer = {}
        self.nubium_topics = {**primary_topics, **internal_topics, **changelog_topics}
        self.cluster_topic_map = cluster_topic_map()
        self.nubium_clusters = [c for c in set(self.cluster_topic_map.values()) if c]
        self.nubium_primary_topic_clusters = {
            cluster: [topic for topic in primary_topics if self.cluster_topic_map[topic] == cluster]
            for cluster in self.nubium_clusters}
        if not configs and self.nubium_clusters:
            configs = [{"bootstrap.servers": server_url} for server_url in self.nubium_clusters]
        if configs and auto_configure:
            self.add_admin_cluster_clients(configs)

    def add_admin_cluster_clients(self, configs):
        """
        Add a new client connection for a given cluster.
        Added to 'self.admin_clients', where k:v is cluster_bootstrap_url: cluster_client_instance.

        By default, uses your environment to establish the client aside from the cluster URLS.

        You can provide configs in the following ways:
            {cluster1_confluent_config_dict}
            'cluster1_bootstrap_url'
        or lists of either.
        """
        if isinstance(configs, list):
            for config in configs:
                self.add_admin_cluster_clients(configs=config)
        else:
            if isinstance(configs, dict):
                server_url = configs.pop("bootstrap.servers")
            else:
                server_url = configs

            if server_url not in self.admin_clients:
                sleep(.2)
                apply_config = {
                    "bootstrap.servers": server_url
                }
                if 'localhost' not in server_url:
                    apply_config.update({
                        "sasl.username": env_vars().get("RHOSAK_USERNAME"),
                        "sasl.password": env_vars().get("RHOSAK_PASSWORD"),
                        "security.protocol": "sasl_ssl",
                        "sasl.mechanisms": "PLAIN",
                    })
                if isinstance(configs, dict):
                    apply_config.update(configs)
                client = AdminClient(apply_config)
                self.admin_clients[apply_config['bootstrap.servers']] = client

    def create_all_topics(self):
        """Creates all the topics by passing the whole topic map to create_topics."""
        self.create_topics(self.cluster_topic_map)

    def create_topics(self, topic_cluster_dict, num_partitions=3, replication_factor=3, topic_config=None,
                      ignore_nubium_topic_cluster_maps=False):
        """
        Accepts a "topic_cluster_dict" like: {'topic_a': 'cluster_url_x', 'topic_b': 'cluster_url_y', 'topic_c': ''}
        If cluster url is provided, will default to that; else, will attempt to derive using nubium_schemas
        if "use_nubium_topic_cluster_maps" is True.
        Otherwise, if "ignore_nubium_topic_cluster_maps" is False, creates topic with predefined nubium_schemas configs.
        Else, will use the args "num_partitions", "replication_factor", "topic_config".
        """
        topic_dict = {clust: [] for clust in self.nubium_clusters}
        for topic, clust in topic_cluster_dict.items():
            if ignore_nubium_topic_cluster_maps:
                topic_dict[clust].append(
                    NewTopic(
                        topic=topic,
                        num_partitions=num_partitions,
                        replication_factor=replication_factor,
                        config=topic_config if topic_config else {}
                    )
                )
            else:
                topic_dict[clust if clust else self.cluster_topic_map[topic]].append(
                    NewTopic(
                        topic=topic,
                        num_partitions=primary_topics[topic].partitions,
                        replication_factor=primary_topics[topic].replication_factor,
                        config=primary_topics[topic].config
                    )
                )
        for clust, topics in topic_dict.items():
            if topics:
                self.add_admin_cluster_clients(clust)
                for topic in topics:
                    try:
                        _wait_on_futures_map(self.admin_clients[clust].create_topics([topic]))
                        print(f"Topic created: {topic}")
                    except KafkaException as e:
                        if e.args[0].code() == KafkaError.TOPIC_ALREADY_EXISTS:
                            print(f"Topic already exists: {topic}")
                            pass

    def delete_topics(self, topic_cluster_dict, ignore_nubium_topic_cluster_maps=False):
        """
        Accepts a "topic_cluster_dict" like: {'topic_a': 'cluster_url_x', 'topic_b': 'cluster_url_y', 'topic_c': ''}
        If cluster url is provided, will default to that; else, will attempt to derive using nubium_schemas
        if "ignore_nubium_topic_cluster_maps" is False.
        """
        topic_dict = {clust: [] for clust in self.nubium_clusters}
        for topic, clust in topic_cluster_dict.items():
            if topic not in primary_topics or ignore_nubium_topic_cluster_maps:
                topic_dict[clust].append(topic)
            else:
                topic_dict[clust if clust else self.cluster_topic_map[topic]].append(topic)
        for clust, topics in topic_dict.items():
            if topics:
                self.add_admin_cluster_clients(server_urls=clust)
                for topic in topics:
                    try:
                        _wait_on_futures_map(self.admin_clients[clust].delete_topics([topic]))
                        print(f"Topic deleted: {topic}")
                    except KafkaException as e:
                        if e.args[0].code() == KafkaError.UNKNOWN_TOPIC_OR_PART:
                            print(f"Topic deletion failed (likely because it didn't exist): {topic}")
                            pass

    def list_topics(self, by_topic=False, mirrors=False, cluster=None):
        """
        Allows you to list all topics across all cluster instances.

        If you want to return the output in a format that is used by the other toolbox functions, then
        you can change "by_topic"=True; the default format makes it easier to read.

        Will not include the mirrored topics by default, but can toggle with "mirrors".
        """
        def _mirror_include(topic):
            if topic.startswith('nubium_'):
                return mirrors
            return True

        def _valid(topic):
            return not topic.startswith('__') and 'schema' not in topic

        if cluster:
            self.add_admin_cluster_clients(cluster)
        else:
            self.add_admin_cluster_clients(self.nubium_clusters)
        by_cluster = {clust: [topic for topic in list(client.list_topics().topics) if _valid(topic) and _mirror_include(topic)]
                      for clust, client in self.admin_clients.items()}
        if by_topic:
            topics = {topic: clust for clust, topics in by_cluster.items() for topic in topics}
            return {k: topics[k] for k in sorted(topics.keys())}
        return {k: sorted(by_cluster[k]) for k in sorted(by_cluster.keys())}

    def produce_messages(self, topic, message_list, schema=None, cluster=None):
        """
        Produce a list of messages (each of which is a dict with entries 'key', 'value', 'headers') to a topic.

        Must provide the schema if you haven't produced to that topic on this instance, or if using dude CLI.
        """
        # TODO extra producer error handling?
        if not self.producers.get(topic):
            if not schema:
                raise ValueError('Schema not provided and the topic producer instance was not previously configured. '
                                 'Please provide the schema!')
            if cluster:
                self.add_admin_cluster_clients(cluster)
            else:
                self.add_admin_cluster_clients(self.cluster_topic_map[topic])
            self.producers.update(get_producers({topic: schema}, return_as_singular=False, cluster=cluster if cluster else None))
        # validate(message, schema)  # Not sure we need this?
        producer = self.producers[topic]
        for message in message_list:
            produce_message(
                producer=producer,
                producer_kwargs=message,
                metrics_manager=MagicMock())  # TODO: change NU to allow a None here? dunno
        producer.flush()

    def consume_messages(self, topic, cluster=None):
        """
        Consume a list of messages (each of which is a dict with entries 'key', 'value', 'headers') from a topic.
        """
        if not self.consumer.get(topic):
            if cluster:
                self.add_admin_cluster_clients(cluster)
            else:
                self.add_admin_cluster_clients(self.cluster_topic_map[topic])
            self.consumer = get_consumer(topic, cluster=cluster if cluster else None)

        try:
            messages = consume_all_messages(consumer=self.consumer, metric_manager=MagicMock())
            enqueue_auto_commits(self.consumer, messages)
            shutdown_cleanup(consumer=self.consumer)
            return messages

        except NoMessageError as e:
            handle_no_messages(e)

        except SignalRaise:
            raise

        except Exception as error:
            log_and_raise_error(MagicMock(), error)


    # def wipe_topic(self, topic):
    #     topics = self.admin_clients[''].list_topics().topics
    #     topic_to_recreate = topics[topic]
    #     partitions = topic_to_recreate.partitions.values()
    #     replicas = set(itertools.chain.from_iterable(p.replicas for p in partitions))
    #     self.admin_clients[''].delete_topic(topic)
    #     while True:
    #         try:
    #             # until KIP-516 is implemented, success of topic creation seems
    #             # to be the only way to detect topic deletion is finished.
    #             self.admin_clients[''].create_topics(topic, num_partitions=len(partitions), replication_factor=len(replicas))
    #             break
    #         except:  # pylint: disable=bare-except
    #             sleep(0.1)


def _wait_on_futures_map(futures):
    for future in futures.values():
        future.result()
        assert future.done()
        sleep(.1)
