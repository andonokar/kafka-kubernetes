from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import (
    SerializationContext,
    MessageField,
)
from time import sleep
from datetime import datetime

# Define the schema for Avro serialization
avro_schema_str = """
{
    "type": "record",
    "name": "User",
    "fields": [
        {"name": "data_hora", "type": "string"},
        {"name": "nome_arquivo", "type": "string"},
        {"name": "mensagem", "type": "string"},
        {"name": "log_mensagem", "type": "string"},
        {"name": "S3_ini", "type": "string"},
        {"name": "S3_fim", "type": "string"},
        {"name": "cliente", "type": "string"},
        {"name": "etapa", "type": "string"}
    ]
}
"""
# Load the Avro schema
schema_registry_conf = {'url': 'http://schema-registry:8081'}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)
avro_serializer = AvroSerializer(schema_registry_client, avro_schema_str)
# Create AvroProducer
avro_producer = Producer(
    {
        "bootstrap.servers": "my-cluster-kafka-bootstrap:9092",
    }
)
for i in range(10000):
    message_payload = {
        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "nome_arquivo": f"{i}",
        "mensagem": "deu certo",
        "log_mensagem": "info",
        "S3_ini": 'bucketinicial',
        "S3_fim": 'bucketfinal',
        "cliente": 'affix',
        "etapa": 'landingzone'
    }
    avro_producer.produce(topic='teste-sink', value=avro_serializer(message_payload, SerializationContext("teste-sink", MessageField.VALUE)))
    avro_producer.flush()  # Wait for the message to be sent
    print(f'mensagem publicada com sucesso:{i}')
    sleep(10)
