import sys
import time
import requests
from kafka import KafkaProducer
from kafka_config import get_credentials


# Function to fetch a joke from the API
def fetch_joke():
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        response.raise_for_status()  # Raises stored HTTPError, if one occurred.
        joke = response.json()
        # return f"{joke['setup']} - {joke['punchline']}"
        return joke
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
