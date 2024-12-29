from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import json
import time
import sys

KAFKA_BROKER = "kafka:9092"
TOPIC = "test_topic"


def create_producer(retries=10, delay=5):
    for attempt in range(retries):
        try:
            print(f"Attempt {attempt + 1} to connect to Kafka broker...")
            producer = KafkaProducer(
                bootstrap_servers=[KAFKA_BROKER],
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
            print("Kafka producer connected successfully!")
            return producer
        except NoBrokersAvailable as e:
            print(f"Kafka broker not available: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
        except Exception as e:
            print(f"Unexpected error while connecting to Kafka: {e}")
            time.sleep(delay)
    print("Failed to connect to Kafka broker after multiple attempts.")
    sys.exit(1)


def send_message(producer, topic, message):
    try:
        producer.send(topic, message)
        print(f"Sent message: {message}")
    except Exception as e:
        print(f"Failed to send message: {message}. Error: {e}")


if __name__ == "__main__":
    kafka_producer = create_producer()

    for i in range(10):
        kafka_message = {"name": "Tester Testovic", "age": i, "city": "Vienna"}
        send_message(kafka_producer, TOPIC, kafka_message)
        time.sleep(1)

    try:
        kafka_producer.flush()
        print("Flushed all pending messages.")
    except Exception as exc:
        print(f"Error while flushing messages: {exc}")
    finally:
        kafka_producer.close()
        print("Closed Kafka producer.")
