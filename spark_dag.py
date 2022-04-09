from airflow.models import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
#from airflow.contrib.operators.spark.spark_submit import SparkSubmitOperator
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
from datetime import datetime ,timedelta
import os
import sys
default_args={
	'owner': 'yasmine',
	#'start_date':datetime(2022,4,9),
	'retries':0,
	'retry_delay':timedelta(minutes=5),
	}



with DAG('spark_dag',
    default_args=default_args,
    schedule_interval='* * * * *',
    start_date=days_ago(2),
    
) as dag:
    # [START howto_operator_spark_submit]
    os.environ['SPARK_HOME'] = '/opt/spark'
    sys.path.append(os.path.join(os.environ['SPARK_HOME'], 'bin'))
    Start_zookeeper= BashOperator(
        task_id="Start_zookeeper",
        bash_command='/usr/local/kafka/bin/zookeeper-server-start.sh config/zookeeper.properties'
    )
    Start_kafka= BashOperator(
        task_id="Start_kafka",
        bash_command='/usr/local/kafka/bin/kafka-server-start.sh config/server.properties'
    )

    Run_producer = BashOperator(
        task_id="Run_producer",
        bash_command='spark-submit --packages org.apache.kafka:kafka_2.11:0.10.0.0,org.apache.kafka:kafka-clients:0.10.0.0 /home/yasmine/kafka_spark/producer1.py'
    )

    Run_consumer = BashOperator(
        task_id="Run_consumer",
        bash_command='spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.3.0,com.datastax.spark:spark-cassandra-connector_2.11:2.3.0 /home/yasmine/kafka_spark/consumer3.py'
    )

    Run_producer >> Run_consumer
    # [END howto_operator_spark_submit]
