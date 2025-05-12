from pyflink.table import EnvironmentSettings, TableEnvironment
import yaml
import os

# Load config
with open(os.path.join("config", "app_config.yaml"), "r") as f:
    config = yaml.safe_load(f)

env_settings = EnvironmentSettings.in_streaming_mode()
t_env = TableEnvironment.create(env_settings)

# Register Kafka source
t_env.execute_sql(f"""
CREATE TABLE clicks (
    user_id BIGINT,
    click_time TIMESTAMP(3),
    product_id STRING,
    WATERMARK FOR click_time AS click_time - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = '{config["kafka"]["click_topic"]}',
    'properties.bootstrap.servers' = '{config["kafka"]["bootstrap_servers"]}',
    'format' = 'json',
    'scan.startup.mode' = 'earliest-offset'
)
""")

# Register ClickHouse sink
t_env.execute_sql(f"""
CREATE TABLE attributed_checkouts (
    user_id BIGINT,
    checkout_time TIMESTAMP(3),
    click_time TIMESTAMP(3),
    product_id STRING,
    attribution_type STRING
) WITH (
    'connector' = 'jdbc',
    'url' = '{config["clickhouse"]["jdbc_url"]}',
    'table-name' = '{config["clickhouse"]["table"]}',
    'driver' = 'com.clickhouse.jdbc.ClickHouseDriver'
)
""")

# Simple select for now
t_env.execute_sql("""
INSERT INTO attributed_checkouts
SELECT user_id, click_time, click_time, product_id, 'click' FROM clicks
""")
