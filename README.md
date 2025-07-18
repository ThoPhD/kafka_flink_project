# Kafka Flink Project

This project demonstrates the integration of Apache Kafka and Apache Flink for real-time data processing. It provides an example of how to consume, process, and produce data streams using these technologies.

## Features
- Real-time data ingestion with Kafka.
- Stream processing with Flink.
- Fault-tolerant and scalable architecture.

## Prerequisites
- Java 8 or higher
- Apache Kafka
- Apache Flink
- Docker and Docker Compose

## Getting Started
1. Clone the repository:
    ```bash
    git clone git@github.com:ThoPhD/kafka_flink_project.git
    ```
2. Navigate to the project directory:
    ```bash
    cd kafka_flink_project
    ```
3. Start Kafka and Flink services.

## Running with Docker Compose
1. Ensure Docker and Docker Compose are installed on your system.
2. Start the services using Docker Compose:
    ```bash
    docker-compose up -d
    ```
3. Verify that Kafka, Flink, and other services are running:
    ```bash
    docker-compose ps
    ```

## Generating Fake Data for Kafka Topics
1. Use the provided Python script or any data generator tool to produce fake data. For example:
    ```bash
    python datagen/gen_data.py
    ```
    or 
    ```bash
    python3 datagen/gen_data.py
    ```
2. Ensure the script is configured to send data to the appropriate Kafka topic.

## Usage
- Configure Kafka topics and Flink job parameters in the `application.properties` file.
- Run the Flink job:
  ```bash
  docker exec -it  flink-jobmanager bash
  flink run -py /opt/flink/jobs/simple_job.py
  ```
