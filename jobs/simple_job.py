from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common import SimpleStringSchema
from pyflink.datastream.connectors import FlinkKafkaConsumer
from pyflink.common.serialization import Encoder
from pyflink.datastream.connectors import FileSink
from pyflink.common.typeinfo import Types

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)

# Dummy stream
ds = env.from_collection(
    collection=["hello", "world", "from", "pyflink"],
    type_info=Types.STRING()
)

# Print to console sink (or file sink if needed)
ds.print()

env.execute("simple_flink_job")
