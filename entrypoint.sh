#!/bin/bash
echo ">>> Starting Flink Cluster"
start-cluster.sh

echo ">>> Sleeping to wait for JobManager"
sleep 10  # Đợi JobManager khởi động

echo ">>> Submitting jobs..."
for job in /opt/flink/jobs/*.py; do
    echo "Running $job"
    flink run -py "$job"
done

echo ">>> All jobs submitted"

tail -f /dev/null
