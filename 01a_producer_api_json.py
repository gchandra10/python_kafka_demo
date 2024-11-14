import sys, time
import time, json
import requests
from kafka import KafkaProducer
from kafka_config import get_credentials
from kafka.admin import KafkaAdminClient
from kafka.admin import NewTopic


# Function to fetch a joke from the API
def fetch_joke():
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        response.raise_for_status()  # Raises stored HTTPError, if one occurred.
        joke = response.json()
        return json.dumps(joke)
    except requests.RequestException as e:
        print(f"Error fetching joke: {e}")
        return None

## Don't use this in Production. 
def delete_and_create_topic(bootstrap_servers: str, topic_name: str):
    # Create admin client
    admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
    
    try:
        # Check if topic exists
        existing_topics = admin_client.list_topics()
        if topic_name in existing_topics:
            # Delete topic
            admin_client.delete_topics([topic_name])
            time.sleep(10)
            
            # Recreate topic
            topic = NewTopic(name=topic_name,
                num_partitions=3,
                replication_factor=1)

            admin_client.create_topics([topic])
            
    except Exception as e:
        print(e)
    finally:
        admin_client.close()


username, password, broker = get_credentials()
delete_and_create_topic(broker,"gctopic")

producer = KafkaProducer(
    bootstrap_servers=broker,
    # sasl_mechanism="SCRAM-SHA-256",
    # security_protocol="SASL_SSL",
    # sasl_plain_username=username,
    # sasl_plain_password=password,
)

try:
    while True:  # Loop indefinitely
        joke = fetch_joke()
        if joke:
            # Encoding to bytes as KafkaProducer expects byte strings
            producer.send("gctopic", joke.encode())
            producer.flush()
            print(f"Produced joke: {joke}")
        else:
            print("No joke to send.")

        # Wait for some time before fetching the next joke
        time.sleep(2)

except KeyboardInterrupt:
    print("Terminating the producer.")
finally:
    producer.close()
