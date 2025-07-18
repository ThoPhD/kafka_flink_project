from pyflink.table import (
    EnvironmentSettings,
    TableEnvironment,
)

# Set up environment
env_settings = EnvironmentSettings.in_streaming_mode()
t_env = TableEnvironment.create(env_settings)


# Kafka clicks source
t_env.execute_sql("""
CREATE TABLE clicks (
    click_id STRING,
    user_id BIGINT,
    click_time TIMESTAMP(3),
    product_id STRING,
    product_name STRING,
    price DECIMAL(5, 2),
    url STRING,
    user_agent STRING,
    ip_address STRING,
    processing_time AS PROCTIME(),
    WATERMARK FOR click_time AS click_time - INTERVAL '15' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'clicks',
    'properties.bootstrap.servers' = 'kafka:9092',
    'properties.group.id' = 'flink-group',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'json'
)
""")
