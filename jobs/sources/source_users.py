from pyflink.table import (
    EnvironmentSettings,
    TableEnvironment,
)

# Set up environment
env_settings = EnvironmentSettings.in_streaming_mode()
t_env = TableEnvironment.create(env_settings)


# Kafka checkouts source
t_env.execute_sql("""
CREATE TEMPORARY TABLE users (
    id INT,
    username STRING,
    PASSWORD STRING,
    PRIMARY KEY (id) NOT ENFORCED
) WITH (
    'connector' = '{{ connector }}',
    'url' = '{{ url }}',
    'table-name' = '{{ table_name }}',
    'username' = '{{ username }}',
    'password' = '{{ password }}',
    'driver' = '{{ driver }}'
)
""")
