from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings

env = StreamExecutionEnvironment.get_execution_environment()
settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
t_env = StreamTableEnvironment.create(env, environment_settings=settings)

# Tạo source table từ collection (dữ liệu nhỏ test)
t_env.execute_sql("""
CREATE TEMPORARY TABLE input_table (
    name STRING,
    age INT
) WITH (
    'connector' = 'datagen',
    'rows-per-second' = '5',
    'fields.name.length' = '5',
    'fields.age.min' = '20',
    'fields.age.max' = '50'
)
""")

# Tạo sink table in ra console
t_env.execute_sql("""
CREATE TEMPORARY TABLE print_table (
    name STRING,
    age INT
) WITH (
    'connector' = 'print'
)
""")

# Chạy job
t_env.execute_sql("""
INSERT INTO print_table
SELECT name, age FROM input_table
""")
