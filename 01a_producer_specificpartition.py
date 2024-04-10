import sys
import time
import requests
import uuid
from kafka import KafkaProducer
from kafka_config import get_credentials

# Function to fetch a joke from the API
def fetch_joke():
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        response.raise_for_status()  # Raises stored HTTPError, if one occurred.
        joke = response.json()
        return f"{joke['setup']} - {joke['punchline']}"
    except requests.RequestException as e:
        print(f"Error fetching joke: {e}")
        return None

username, password = get_credentials()

producer = KafkaProducer(
    bootstrap_servers="helping-hen-9837-us1-kafka.upstash.io:9092",
    sasl_mechanism="SCRAM-SHA-256",
    security_protocol="SASL_SSL",
    sasl_plain_username=username,
    sasl_plain_password=password,
)

try:
    while True:  # Loop indefinitely
        joke = fetch_joke()
        if joke:
            # Send the joke to a specific partition, e.g., partition 0
            key = "jokeCategory".encode()  
            key = uuid.uuid4().bytes
            metadata = producer.send("gctopic",key=key, value=joke.encode()).get()
            #producer.flush()
            print(f"Produced joke to partition {metadata.partition} : {joke}")
        else:
            print("No joke to send.")
        
        # Wait for some time before fetching the next joke
        time.sleep(2)  # Sleep for 2 seconds; adjust as needed

except KeyboardInterrupt:
    print("Terminating the producer.")
finally:
    producer.close()
