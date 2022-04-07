#spark-submit --packages org.apache.kafka:kafka_2.11:0.10.0.0,org.apache.kafka:kafka-clients:0.10.0.0 producer1.py

from pyspark import SparkContext
from kafka import KafkaProducer
import time
from random import randint
from time import sleep
import sys


BROKER ='localhost:9092'
TOPIC= 'tweets'
WORD_FILE = '/usr/share/dict/words'
WORDS=open(WORD_FILE).read().split("\n")
sc = SparkContext("local[1]", "KafkaSendStream")
p = KafkaProducer(bootstrap_servers='localhost:9092')
#try:
	#p=KafkaProducer(bootstrap_servers=BROKER)
#except Exception as e:
	#print(e)
	#sys.exit(1)

while True:
	message =''
	for _ in range(randint(2,7)):
		message += WORDS[randint(0,len(WORDS)-1)] + ' '
	print(message)
	p.send(TOPIC, message.encode('UTF-8'))
	sleep(randint(1,4))
