# Setup

## Kafka-python Documentation 

https://kafka-python.readthedocs.io/en/master/usage.html

## Install the Python Library

#### poetry add git+https://github.com/dpkp/kafka-python.git

## Create a FREE account for Kafka

https://console.upstash.com/login

Goto Kafka & Deploy a Cluster and create 2 topics

gctopic - 1 partition
gctopic_m - 2 partitions

## Simple Example.

- poetry run 01_producer_simple.py message
- poetry run 02_consumer_simple_autocommit.py

## Read from an API and push it to Kafka

- poetry run 01a_producer_api_json.py
- poetry run 02_consumer_simple_autocommit.py

## Read from an API and push it to Kafka multiple partitions

- poetry run 01b_producer_multipartition.py
- poetry run 02_consumer_simple_autocommit.py

## Read from an API and stream in Batch

- poetry run 01c_producer_batch.py
- poetry run 02c_consumer_batch.py