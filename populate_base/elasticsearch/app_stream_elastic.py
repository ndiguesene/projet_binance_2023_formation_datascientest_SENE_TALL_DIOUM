import json

from confluent_kafka import Consumer, KafkaException
from elasticsearch import Elasticsearch

from constant import INDEX_ELASTIC

# Configuration du consommateur Kafka
conf = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'my-group',
    'auto.offset.reset': 'latest'  # Commencer à lire à la fin du topic
}

consumer = Consumer(conf)

# Configuration d'Elasticsearch
es = Elasticsearch('http://localhost:9200')
consumer.subscribe(['cryptobot'])

try:
    while True:
        msg = consumer.poll(timeout=1.0)  # Récupération des messages du topic
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaException._PARTITION_EOF:
                continue
            else:
                print(f"Erreur rencontrée : {msg.error()}")
                break

        # Traitement du message reçu depuis Kafka
        message_data = msg.value().decode('utf-8')
        parsed_message = json.loads(message_data)

        # Envoi des données à Elasticsearch
        es.index(index=INDEX_ELASTIC,
                 body=parsed_message)  # Remplacez 'nom_de_votre_index' par votre index Elasticsearch
except KeyboardInterrupt:
    pass

finally:
    # Fermeture du consommateur Kafka
    consumer.close()
