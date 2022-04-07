"""
spark-submit --packages org.apache.spark:spark-streaming-kafka_2.10:1.5.0,TargetHolding/pyspark-cassandra:0.1.5 --conf spark.cassandra.connection.host=127.0.0.1 example.py my-topic
"""

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
#import pyspark_cassandra
from pyspark_cassandra import streaming
from datetime import datetime
import sys

# Create a StreamingContext with batch interval of 3 second
sc = SparkContext("spark://MASTER:7077", "myAppName")
ssc = StreamingContext(sc, 3)

topic = sys.argv[1]
kafkaStream = KafkaUtils.createStream(ssc, "MASTER_IP:2181", "topic", {topic: 4})

raw = kafkaStream.flatMap(lambda kafkaS: [kafkaS])
time_now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
clean = raw.map(lambda xs: xs[1].split(","))

# Test timestamp 1 and timestamp 2
# times = clean.map(lambda x: [x[1], time_now])
# times.pprint()

# test subtract new time from old time
# x = clean.map(lambda x:
#             (datetime.strptime(x[1], '%Y-%m-%d %H:%M:%S.%f') -
#             datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S.%f')).seconds)
# x.pprint()


# Match table fields with dictionary keys
# this reads input of format
# partition, timestamp, location, price
my_row = clean.map(lambda x: {
      "testid": "test",
      "time1": x[1],
      "time2": time_now,
      "location": x[2],
      "delta": (datetime.strptime(x[1], '%Y-%m-%d %H:%M:%S.%f') -
       datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S.%f')).microseconds,
      "brand": "brand",
      "price": round(float(x[3]), 2) })
# my_row.pprint()

my_row.saveToCassandra("KEYSPACE", "TABLE_NAME")

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
