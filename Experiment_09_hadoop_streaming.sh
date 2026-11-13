#!/usr/bin/env bash
set -euo pipefail

HADOOP_STREAMING_JAR="${HADOOP_STREAMING_JAR:-$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.9.2.jar}"
MONGO_HADOOP_CORE="${MONGO_HADOOP_CORE:-/path/to/mongo-hadoop-core.jar}"
MONGO_HADOOP_STREAMING="${MONGO_HADOOP_STREAMING:-/path/to/mongo-hadoop-streaming.jar}"
MONGO_JAVA_DRIVER="${MONGO_JAVA_DRIVER:-/path/to/mongo-java-driver.jar}"

hdfs dfs -mkdir -p /user/$USER/transactions
hdfs dfs -put -f datasets/transactions.csv /user/$USER/transactions/

hadoop jar "$HADOOP_STREAMING_JAR" \
  -libjars "$MONGO_HADOOP_CORE,$MONGO_HADOOP_STREAMING,$MONGO_JAVA_DRIVER" \
  -D mongo.output.uri=mongodb://localhost:27017/bigdata_db.transactions \
  -D mapreduce.job.reduces=0 \
  -input  /user/$USER/transactions/transactions.csv \
  -output /user/$USER/transactions_out \
  -mapper "python3 Experiment_09_mapper.py" \
  -file Experiment_09_mapper.py \
  -outputformat com.mongodb.hadoop.mapred.MongoOutputFormat
