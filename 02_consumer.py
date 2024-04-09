# pip3 install git+https://github.com/dpkp/kafka-python.git

from kafka import KafkaConsumer, TopicPartition

from kafka_config import get_credentials

username, password = get_credentials()

consumer = KafkaConsumer(
    "gctopic",
    bootstrap_servers="helping-hen-9837-us1-kafka.upstash.io:9092",
    sasl_mechanism="SCRAM-SHA-256",
    security_protocol="SASL_SSL",
    sasl_plain_username=username,
    sasl_plain_password=password,
    group_id="gcgroup1",
    auto_offset_reset="earliest",
)

try:
    for message in consumer:
        message_str = message.value.decode("utf-8")
        print(f"Received message: {message_str}")
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
