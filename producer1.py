from kafka import KafkaProducer
from random import randint
from time import sleep
import sys


BROKER ='localhost:9092'
TOPIC= 'tweets'
WORD_FILE = '/usr/share/dict/words'
WORDS=open(WORD_FILE).read().split("\n")

try:
	p=KafkaProducer(bootstrap_servers=BROKER)
except Exception as e:
	print(e)
	sys.exit(1)

while True:
	message =''
	for _ in range(randint(2,7)):
		message += WORDS[randint(0,len(WORDS)-1)] + ' '
	print(message)
	p.send(TOPIC, message.encode('UTF-8'))
	sleep(randint(1,4))
