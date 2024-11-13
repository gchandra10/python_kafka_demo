# Setup

## Kafka-python Documentation 

https://kafka-python.readthedocs.io/en/master/usage.html

## Install the Python Library

```
poetry add git+https://github.com/dpkp/kafka-python.git
```

[Configure Kafka via Docker](https://bigdatabook.gchandra.com/chapter_08/kafka/kafka-software.html)

```
Make sure docker_compose.yaml is available 
podman-compose up -d
```

## Simple Example.

```
poetry run python 01_producer_simple.py message

poetry run python 02_consumer_simple_autocommit.py
```

## Read from an API and push it to Kafka

```
poetry run python 01a_producer_api_json.py

poetry run python 02_consumer_simple_autocommit.py
```

## Read from an API and push it to Kafka multiple partitions

```
poetry run python 01b_producer_multipartition.py
poetry run python 02_consumer_simple_autocommit.py
```

## Read from an API and stream in Batch

```
poetry run python 01c_producer_batch.py
poetry run python 02c_consumer_batch.py
```