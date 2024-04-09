import sys
from kafka import KafkaProducer
from kafka_config import get_credentials

# Make sure there's at least one command line argument
if len(sys.argv) < 2:
    print("Usage: script.py <message>")
    sys.exit(1)

# The message to send is the first command line argument
message = sys.argv[1].encode()  # Encoding to bytes as KafkaProducer expects byte strings

username, password = get_credentials()

## SCRAM (Salted Challenge Response Authentication Mechanism) is an authentication protocol
## SASL (Simple Authentication and Security Layer) is a framework that provides a mechanism for 
# adding authentication support to connection-based protocols. 

producer = KafkaProducer(
    bootstrap_servers="helping-hen-9837-us1-kafka.upstash.io:9092",
    sasl_mechanism="SCRAM-SHA-256",
    security_protocol="SASL_SSL",
    sasl_plain_username=username,
    sasl_plain_password=password,
)

try:
    producer.send("gctopic", message)
    producer.flush()

except Exception as e:
    print(f"Error producing message: {e}")
finally:
    producer.close()
