import sys, time, requests
import uuid
import json
from kafka import KafkaProducer
from kafka_config import get_credentials


# Function to fetch a joke from the API
def fetch_joke():
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        response.raise_for_status()  # Raises stored HTTPError, if one occurred.
        joke = response.json()
        #return f"{joke['setup']} - {joke['punchline']}"
        return json.dumps(joke)
    except requests.RequestException as e:
        print(f"Error fetching joke: {e}")
        return None

username, password, broker = get_credentials()

producer = KafkaProducer(
    bootstrap_servers=broker,
    sasl_mechanism="SCRAM-SHA-256",
    security_protocol="SASL_SSL",
    sasl_plain_username=username,
    sasl_plain_password=password,
)

try:
    while True:  # Loop indefinitely
        joke = fetch_joke()
        print(joke)
        if joke:

            # Key can be a single hard coded value
            # key = "jokeCategory".encode()

            # Dynamic uuid for universal uniqueness
            key = uuid.uuid4().bytes

            # Send the joke to a specific partition, e.g., partition 0
            # metadata = producer.send("gctopic",key=key, value=joke.encode(), partition=0).get()

            ## Sends messages to available partitions randomly
            metadata = producer.send("gctopic_m", key=key, value=joke.encode()).get()

            # producer.flush()
            print(f"Produced joke to partition {metadata.partition} : {joke}")
        else:
            print("No joke to send.")

        # Wait for some time before fetching the next joke
        time.sleep(2)  # Sleep for 2 seconds; adjust as needed

except KeyboardInterrupt:
    print("Terminating the producer.")
finally:
    producer.close()
