from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from app.logs.app_logger import FILE_NAME
import json

def produce(topic: str, log_entry):
    try:
        producer = KafkaProducer(
            bootstrap_servers = 'localhost:9092',
            value_serializer = lambda x : json.dumps(x).encode('utf-8') 
        )
        try:
            producer.send(topic, log_entry)
        except Exception as e:
            print(e)
        producer.flush()
        producer.close()
    except NoBrokersAvailable as e:
        print("\n\t* Kafka Broker Unavailable *\n")

