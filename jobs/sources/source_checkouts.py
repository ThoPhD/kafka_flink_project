from pyflink.table import (
    EnvironmentSettings,
    TableEnvironment,
)

# Set up environment
env_settings = EnvironmentSettings.in_streaming_mode()
t_env = TableEnvironment.create(env_settings)


# Kafka checkouts source
t_env.execute_sql("""
CREATE TABLE checkouts (
    user_id BIGINT,
    checkout_time TIMESTAMP(3),
    product_id STRING,
    WATERMARK FOR checkout_time AS checkout_time - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'checkouts',
    'properties.bootstrap.servers' = 'localhost:9092',
    'properties.group.id' = 'flink-group',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'json'
)
""")
