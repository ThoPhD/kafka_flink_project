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
    checkout_id STRING,
    user_id BIGINT,
    payment_method STRING,
    total_amount DECIMAL(5, 2),
    shipping_address STRING,
    billing_address STRING,
    user_agent STRING,
    ip_address STRING,
    processing_time AS PROCTIME(),
    checkout_time TIMESTAMP(3),
    product_id STRING,
    WATERMARK FOR checkout_time AS checkout_time - INTERVAL '15' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'checkouts',
    'properties.bootstrap.servers' = 'kafka:9092',
    'properties.group.id' = 'flink-group',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'json'
)
""")
