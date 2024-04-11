# Setup

## Kafka-python Documentation 

https://kafka-python.readthedocs.io/en/master/usage.html

## Install the Python Library

#### pip install git+https://github.com/dpkp/kafka-python.git
or
#### pip3 install git+https://github.com/dpkp/kafka-python.git

## Create a FREE account for Kafka

https://console.upstash.com/login

Goto Kafka & Deploy a Cluster and create 2 topics

gctopic - 1 partition
gctopic_m - 2 partitions

## Usage

### Simple Example.

#### python3 01_producer_simple.py message
#### python3 02_consumer_simple_autocommit.py

### Read from an API and push it to Kafka

#### python3 01a_producer_api_json.py
#### python3 02_consumer.py

### Read from an API and push it to Kafka multiple partitions

#### python3 01b_producer_multipartition.py
#### python3 02_consumer.py

### Read from an API and stream in Batch

#### python3 01c_producer_batch.py
#### python3 02c_consumer_batch.py

