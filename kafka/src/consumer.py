from pprint import pprint

import psycopg2
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json

DB_NAME = "testdb"
DB_USER = "user"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"

KAFKA_BROKER = "localhost:9092"
TOPIC = "test_topic"


def connect_postgres():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        raise


def insert_to_db(data):
    try:
        conn = connect_postgres()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                age INTEGER,
                city VARCHAR(255)
            )
        """)

        cur.execute(
            """
            INSERT INTO user_data (name, age, city) VALUES (%s, %s, %s)
        """,
            (data["name"], data["age"], data["city"]),
        )

        conn.commit()
        cur.close()
        conn.close()
        print(f"Data inserted into PostgreSQL: {data}")
    except psycopg2.Error as e:
        print(f"Error inserting data into PostgreSQL: {e}")


def consume_messages_and_store():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset="earliest",  # Start from the earliest message if no offset is committed
        enable_auto_commit=True,
        group_id="test_group",
    )

    print(f"Consumer subscribed to topic: {TOPIC}")

    try:
        for message in consumer:
            try:
                if message.value:
                    pprint("###################### message")
                    pprint(message)

                    data = json.loads(
                        message.value.decode("utf-8")
                    )  # Deserialize from bytes to dict
                    print(f"Deserialized message: {data}")

                    insert_to_db(data)
                    print(f"Message inserted into PostgreSQL: {data}")
                else:
                    print("Received empty message. Skipping...")
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}. Skipping message: {message.value}")
            except Exception as e:
                print(f"Unexpected error: {e}. Skipping message.")
    except KafkaError as e:
        print(f"Kafka error: {e}")
    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        consumer.close()
        print("Consumer closed.")


if __name__ == "__main__":
    consume_messages_and_store()
