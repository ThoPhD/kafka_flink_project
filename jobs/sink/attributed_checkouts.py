from pyflink.table import (
    EnvironmentSettings,
    TableEnvironment,
)

# Set up environment
env_settings = EnvironmentSettings.in_streaming_mode()
t_env = TableEnvironment.create(env_settings)

# Register ClickHouse JDBC sink
t_env.execute_sql("""
CREATE TABLE attributed_checkouts (
    user_id BIGINT,
    checkout_time TIMESTAMP(3),
    click_time TIMESTAMP(3),
    product_id STRING,
    attribution_type STRING
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:clickhouse://localhost:8123/default',
    'table-name' = 'attributed_checkouts',
    'driver' = 'com.clickhouse.jdbc.ClickHouseDriver',
    'username' = 'flinkuser',
    'password' = 'flinkpass'
)
""")

# Simulated result table (you would replace this with your processed Flink logic)
t_env.execute_sql("""
CREATE TEMPORARY TABLE result (
    user_id BIGINT,
    checkout_time TIMESTAMP(3),
    click_time TIMESTAMP(3),
    product_id STRING,
    attribution_type STRING
) WITH (
    'connector' = 'filesystem',
    'path' = 'file:///tmp/fake_result',
    'format' = 'csv'
)
""")

# Insert from result into ClickHouse
t_env.execute_sql("""
INSERT INTO attributed_checkouts
SELECT * FROM result
""")
