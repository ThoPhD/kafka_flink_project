#!/bin/bash
JAR_PATH="clickhouse-jdbc-0.4.6-all.jar"
flink run -py jobs/kafka_to_clickhouse.py --jars $JAR_PATH
