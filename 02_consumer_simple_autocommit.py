# pip3 install git+https://github.com/dpkp/kafka-python.git
import uuid
import datetime
from kafka import KafkaConsumer, TopicPartition

from kafka_config import get_credentials

username, password, broker = get_credentials()

# Consumer does a Auto Commit.
consumer = KafkaConsumer(
    bootstrap_servers=broker,
    sasl_mechanism="SCRAM-SHA-256",
    security_protocol="SASL_SSL",
    sasl_plain_username=username,
    sasl_plain_password=password,
    group_id="gcgroup1",
    auto_offset_reset="earliest",
)

# Change the topicname if needed
consumer.subscribe(["gctopic", "gctopic_m"])

try:
    for message in consumer:

        # message_key = message.key.decode('utf-8') if message.key else 'None'
        message_key = uuid.UUID(bytes=message.key) if message.key else "None"

        # Read the timestamp in milli seconds and divide it by 1000 for seconds
        message_epoch_ts = message.timestamp
        message_ts = datetime.datetime.fromtimestamp(message_epoch_ts / 1000).strftime(
            "%c"
        )

        """
        0 means timestamp when the message was created by the producer.
        1 means timestamp when the message is appended to the log.
        Kafka Admin decides whether to use created time or append time depending on the Business requirement.
        By default its Created Time.
        Logtime is needed when Business is interested when it was added to log instead of when its created.
        """
        message_ts_type = (
            "CreateTime" if message.timestamp_type == 0 else "LogAppendTime"
        )

        # Read the message and convert it to String
        message_str = message.value.decode("utf-8")

        # Accessing the partition number directly
        message_partition = message.partition

        # Accessing the offset
        message_offset = message.offset

        # Get the topic its reading from.
        # Used when reading from multiple topics at the same time
        message_topic = message.topic

        print("-" * 100)
        print(
            f"Topic: {message_topic} \
        \nPartition: {message_partition} \
        \nOffset: {message_offset} \
        \nKey: {message_key} \
        \nTS: {message_ts}, {message_ts_type} \
        \nMessage: {message_str}"
        )

except KeyboardInterrupt:
    pass
finally:
    # Remember to close the consumer.
    # Helps in offset management, avoid memory leaks, main application state (clean restart)
    consumer.close()
