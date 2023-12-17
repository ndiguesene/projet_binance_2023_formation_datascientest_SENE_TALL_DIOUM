from confluent_kafka import Consumer, KafkaException
import sys
import json

# Configuration du consommateur Kafka
conf = {
    'bootstrap.servers': 'kafka:9092',  # Remplacez par vos paramètres de connexion Kafka
    'group.id': 'my-group',  # Spécifiez un ID de groupe pour le consommateur
    'auto.offset.reset': 'latest'  # Commencer à lire les derniers messages du topic
    # 'auto.offset.reset': 'earliest'  # Commencer à lire depuis le début du topic
}

consumer = Consumer(conf)

# Abonnement au topic "cryptobot"
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
        print(f"Message reçu: {parsed_message}")

except KeyboardInterrupt:
    pass

finally:
    # Fermeture du consommateur Kafka
    consumer.close()
