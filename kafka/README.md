# Kafka with Python Producer and PostgreSQL Example
This project demonstrates a simple setup of Apache Kafka, a Python producer application, and PostgreSQL using Docker 
and Docker Compose. The Python application sends test messages to a Kafka topic.

Project Structure
bash
Kopírovať kód
.
├── docker-compose.yml          # Docker Compose file to configure services
├── Dockerfile                  # Dockerfile for building the Python app image
├── requirements.txt            # Python dependencies
├── src/
│   ├── producer.py             # Python Kafka producer script
│   ├── consumer.py             # Python Kafka consumer script
└── README.md                   # Project documentation

## Prerequisites
- Docker installed on your system
- Docker Compose installed on your system

## Getting Started

```bash
git clone https://github.com/tonnas/lab.git

cd lab/kafka

docker-compose up --build
```

This will start:

- Kafka (Bitnami Kafka with KRaft mode)
- PostgreSQL (latest version)
- Python producer app (sends messages to Kafka)

### Verify Kafka Is Running
Kafka will be available on localhost:9092. Use the following command to check if the Kafka topic exists 
(replace test_topic with your topic name):

```bash
docker exec -it kafka-kafka-1 kafka-topics.sh --bootstrap-server localhost:9092 --list
```
If the topic doesn't exist, create it:
```bash
docker exec -it kafka-kafka-1 kafka-topics.sh --bootstrap-server localhost:9092 --cr
```
