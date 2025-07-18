from pyflink.table import EnvironmentSettings, TableEnvironment
import yaml
import os

# === Load Config ===
with open(os.path.join("config", "app_config.yaml"), "r") as f:
    config = yaml.safe_load(f)

# === Set up Table Environment ===
env_settings = EnvironmentSettings.in_streaming_mode()
t_env = TableEnvironment.create(env_settings)

# === Kafka Source: Clicks ===
t_env.execute_sql(f"""
CREATE TABLE clicks (
    click_id STRING,
    user_id BIGINT,
    click_time TIMESTAMP(3),
    product_id STRING,
    product STRING,
    price DECIMAL(10, 2),
    url STRING,
    user_agent STRING,
    ip_address STRING,
    WATERMARK FOR click_time AS click_time - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = '{config["kafka"]["click_topic"]}',
    'properties.bootstrap.servers' = '{config["kafka"]["bootstrap_servers"]}',
    'properties.group.id' = 'flink-group',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'json'
)
""")

# === Kafka Source: Checkouts ===
t_env.execute_sql(f"""
CREATE TABLE checkouts (
    checkout_id STRING,
    user_id BIGINT,
    checkout_time TIMESTAMP(3),
    product_id STRING,
    payment_method STRING,
    total_amount DECIMAL(10, 2),
    shipping_address STRING,
    billing_address STRING,
    user_agent STRING,
    ip_address STRING,
    WATERMARK FOR checkout_time AS checkout_time - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = '{config["kafka"]["checkout_topic"]}',
    'properties.bootstrap.servers' = '{config["kafka"]["bootstrap_servers"]}',
    'properties.group.id' = 'flink-group',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'json'
)
""")

# === Static JDBC Source: Users ===
t_env.execute_sql(f"""
CREATE TABLE users (
    id BIGINT,
    email STRING,
    username String,
    password String
    ) WITH (
    'connector' = 'jdbc',
    'url' = '{config["users"]["jdbc_url"]}',
    'table-name' = '{config["users"]["schema"]}.{config["users"]["table"]}',
    'driver' = '{config["users"]["driver"]}'
)
""")

# === ClickHouse Sink Table: Attributed Checkouts ===
# t_env.execute_sql(f"""
# CREATE TABLE attributed_checkouts (
#     user_id BIGINT,
#     checkout_time TIMESTAMP(3),
#     click_time TIMESTAMP(3),
#     product_id STRING,
#     attribution_type STRING
# ) WITH (
#     'connector' = 'jdbc',
#     'url' = '{config["clickhouse"]["jdbc_url"]}',
#     'table-name' = '{config["users"]["schema"]}.{config["clickhouse"]["table"]}',
#     'driver' = 'com.clickhouse.jdbc.ClickHouseDriver'
# )
# """)

# === View: Join Clicks & Checkouts with Attribution Window and User Enrichment ===
# t_env.execute_sql("""
# CREATE VIEW enriched_attribution AS
# SELECT
#     co.user_id,
#     co.checkout_time,
#     c.click_time,
#     co.product_id,
#     u.email,
#     u.username,
#     'click_attributed' AS attribution_type
# FROM checkouts AS co
# JOIN clicks AS c
#   ON co.user_id = c.user_id
#   AND co.product_id = c.product_id
#   AND c.click_time BETWEEN co.checkout_time - INTERVAL '30' MINUTE AND co.checkout_time
# JOIN users u
#   ON u.id = co.user_id
# """)
t_env.execute_sql("""
CREATE VIEW enriched_attribution AS
SELECT
    co.user_id,
    CAST(co.checkout_time AS TIMESTAMP) AS checkout_time,
    c.click_time,
    co.product_id,
    'click_attributed' AS attribution_type
FROM checkouts AS co
JOIN clicks AS c
  ON co.user_id = c.user_id
  AND co.product_id = c.product_id
  AND c.click_time BETWEEN co.checkout_time - INTERVAL '30' MINUTE AND co.checkout_time
""")
# # === Insert into ClickHouse Sink ===
# t_env.execute_sql("""
# INSERT INTO attributed_checkouts
# SELECT user_id, checkout_time, click_time, product_id, attribution_type
# FROM enriched_attribution
# """)


# Tạo sink table in ra console
t_env.execute_sql("""
CREATE TEMPORARY TABLE attributed_checkouts (
    user_id BIGINT,
    checkout_time TIMESTAMP(3),
    click_time TIMESTAMP(3),
    product_id STRING,
    attribution_type STRING
) WITH (
    'connector' = 'print'
)
""")

# Chạy job
t_env.execute_sql("""
INSERT INTO attributed_checkouts
SELECT user_id, checkout_time, click_time, product_id, attribution_type
FROM enriched_attribution
""")