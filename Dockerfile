FROM flink:scala_2.12

# # Download required JARs
# RUN wget -P /opt/flink https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/1.17.1/flink-sql-connector-kafka-1.17.1.jar \
#     && wget -P /opt/flink https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc/3.1.0-1.17/flink-connector-jdbc-3.1.0-1.17.jar \
#     && wget -P /opt/flink https://github.com/ClickHouse/clickhouse-java/releases/download/v0.4.6/clickhouse-jdbc-0.4.6-patch13-all.jar

# Install Python, pip, and build dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev build-essential libffi-dev libssl-dev curl unzip && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    apt-get clean


# Copy requirements.txt into container
COPY requirements.txt /tmp/requirements.txt

# Install Python packages
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Set python as default
# RUN ln -s /usr/bin/python3 /usr/bin/python

COPY jars/*.jar /opt/flink/lib/
COPY jobs /opt/flink/jobs
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
