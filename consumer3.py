#spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.3.0,com.datastax.spark:spark-cassandra-connector_2.11:2.3.0 consumer3.py
import os
#os.environ['PYSPARK_SUBMIT_ARGS'] = '--conf spark.ui.port=4040 --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.3.0,com.datastax.spark:spark-cassandra-connector_2.11:2.3.0-M3 pyspark-shell'
import time
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, Row
conf = SparkConf() \
    .setAppName("Streaming test") \
    .setMaster("local[2]") \
    .set("spark.cassandra.connection.host", "127.0.0.1")
sc = SparkContext(conf=conf) 
sqlContext=SQLContext(sc)


def saveToCassandra(rows):
    if not rows.isEmpty(): 
        sqlContext.createDataFrame(rows).write\
        .format("org.apache.spark.sql.cassandra")\
        .mode('append')\
        .options(table="tweets1", keyspace="sparkdata")\
        .save()
        
ssc = StreamingContext(sc, 5)
kvs = KafkaUtils.createStream(ssc, "127.0.0.1:2181", "spark-streaming-consumer", {'tweets': 1})

lines=kvs.map(lambda x:x[1])     
lines.count().map(lambda x:'Tweets in this batch: %s' % x).pprint()

rows= lines.map(lambda tweet:Row(tweet, int(len(tweet.split())), int(len(tweet))))
rows.foreachRDD(saveToCassandra)
rows.pprint()
  
ssc.start()                                                                                                          
ssc.awaitTermination()
#ssc.stop(stopSparkContext=False,stopGraceFully=True)

#data=sqlContext.read\
    #.format("org.apache.spark.sql.cassandra")\
    #.options(table="tweets", keyspace="sparkdata")\
    #.load()
#data.show()
