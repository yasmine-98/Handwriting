import time
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, Row, SparkSession
from datetime import datetime, timedelta
import findspark
import os
#os.environ['PYSPARK_SUBMIT_ARGS'] = "--master yarn pyspark-shell" 
findspark.init()

def saveToCassandra(rows):
    if not rows.isEmpty(): 
        sqlContext.createDataFrame(rows).write\
        .format("org.apache.spark.sql.cassandra")\
        .mode('append')\
        .options(table="batchTable", keyspace="test_time")\
        .save()

def current_milli_time():
    return round(time.time() * 1000)

conf = SparkConf() \
    .setAppName("batch_processing") \
    .setMaster("local[*]") \
    .set("spark.cassandra.connection.host", "127.0.0.1")
sc = SparkContext(conf=conf) 
sqlContext=SQLContext(sc) 

#ss = SparkSession.builder.appName("batch_processing") \
#.set("spark.cassandra.connection.host", "127.0.0.1") \
#.getOrCreate()  
#sc = SparkContext.getOrCreate()

sc.setLogLevel("WARN")

#current_time=datetime.now()
current_time=datetime.today()
#current_time = current_time.strftime("%d-%m-%Y %H:%M:%S")
#current_time=datetime(current_time)
#current_time=datetime.strptime(str(current_time),'%Y-%m-%d %H:%M:%S')

print(current_time)
hours = 3
hours_added = timedelta(hours = hours)
print(hours_added)

final_time = current_time - hours_added
print(final_time)
rdd =sc.textFile("hdfs://127.0.0.1:9000/user/datastore")

rdd=rdd.map(lambda l: l.split(","))
rows1= rdd.map(lambda x:Row(id=x[0], txt=x[1],createddate=x[2], words=int(len(x[1].split())), length=int(len(x[1]))))

print(rows1.take(10))
df = rows1.toDF()
x = df.first()[0]
print(x)
df.show()

df1=df.filter(df.createddate>final_time)
df1.show()
df1.write\
.format("org.apache.spark.sql.cassandra")\
.mode('append')\
.options(table="data", keyspace="test_time")\
.save()
#df1.write.format("org.apache.spark.sql.cassandra").options(
#  table="batchTable", keyspace="test_time"
#).save()
#rd=df1.rdd
#rd.saveToCassandra("test_time","batchTable")  

#rows= rd.map(lambda x:Row(id=x[1], txt=x[3],createddate=x[0], words=x[4], length=x[2]))
#print(rows.take(10))

#rows.foreachRDD(saveToCassandra)
#rows.pprint()
#for i in lines.take(10):
	#print(i)
