from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
from time import sleep
# Define the schema for Avro serialization
avro_schema_str = """
{
    "type": "record",
    "name": "User",
    "fields": [
        {"name": "registertime", "type": "long"},
        {"name": "userid", "type": "string"},
        {"name": "regionid", "type": "string"},
        {"name": "gender", "type": "string"}
    ]
}
"""
# Load the Avro schema
avro_schema = avro.loads(avro_schema_str)
# Create AvroProducer
avro_producer = AvroProducer(
    {
        "bootstrap.servers": "my-cluster-kafka-bootstrap:9092",
        "schema.registry.url": "http://schema-registry:8081",  # Replace with your Schema Registry URL
    },
    default_value_schema=avro_schema,
)
for i in range(10000):
    message_payload = {
        "registertime": 1493819497170,
        "userid": f"User_{i}",
        "regionid": "Region_5",
        "gender": "MALE"
    }
    avro_producer.produce(topic='teste-sink', value=message_payload)
    avro_producer.flush()  # Wait for the message to be sent
    print(f'mensagem publicada com sucesso:{i}')
    sleep(10)
