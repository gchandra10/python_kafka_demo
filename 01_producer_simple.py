import sys, time
from kafka import KafkaProducer
from kafka_config import get_credentials
from kafka.admin import KafkaAdminClient
from kafka.admin import NewTopic

# Make sure there's at least one command line argument
if len(sys.argv) < 2:
    print("Usage: script.py <message>")
    sys.exit(1)

# The message to send is the first command line argument
message = sys.argv[1].encode()  # Encoding to bytes as KafkaProducer expects byte strings

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

## SCRAM (Salted Challenge Response Authentication Mechanism) is an authentication protocol
## SASL (Simple Authentication and Security Layer) is a framework that provides a mechanism for
# adding authentication support to connection-based protocols.

producer = KafkaProducer(
    bootstrap_servers=broker
    # sasl_mechanism="SCRAM-SHA-256",
    # security_protocol="SASL_SSL",
    # sasl_plain_username=username,
    # sasl_plain_password=password,
)

try:
    producer.send("gctopic", message)

    # Forces all buffered messages to be sent to the Kafka broker immediately
    # As a best practice its good to call flush() before calling the close()

    producer.flush()

except Exception as e:
    print(f"Error producing message: {e}")
finally:
    producer.close()
