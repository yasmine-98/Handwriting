#spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.3.0,com.datastax.spark:spark-cassandra-connector_2.11:2.3.0 consumer3.py
import time
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, Row
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


def saveToCassandra(rows):
    if not rows.isEmpty(): 
        sqlContext.createDataFrame(rows).write\
        .format("org.apache.spark.sql.cassandra")\
        .mode('append')\
        .options(table="tweets1", keyspace="test_time")\
        .save()

    
conf = SparkConf() \
    .setAppName("Streaming test") \
    .setMaster("local[2]") \
    .set("spark.cassandra.connection.host", "127.0.0.1")
sc = SparkContext(conf=conf) 
sqlContext=SQLContext(sc)    
        
ssc = StreamingContext(sc, 5)
kvs = KafkaUtils.createStream(ssc, "127.0.0.1:2181", "spark-streaming-consumer", {'tweets': 1})
data = kvs.map(lambda x: x[1])

rows= data.map(lambda x:Row(txt=x, length=int(len(x)), words=int(len(x.split()))))
                                                                                                         
rows.foreachRDD(saveToCassandra)
rows.pprint()
ssc.start()
ssc.awaitTermination()
