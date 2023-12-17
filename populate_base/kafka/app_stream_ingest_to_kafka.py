import os

from binance.client import Client
from confluent_kafka import Producer
import json

# Configuration de l'API Binance en récuparant les variables d'enrivonnement
api_key = os.getenv("api_key")
api_secret = os.getenv("api_secret")
bootstrap_servers = os.getenv("SERVERS")
topic_name = os.getenv("topic_name")

client = Client(api_key=api_key, api_secret=api_secret, testnet=False)  # Changer testnet à True pour le testnet

producer = Producer({
    'bootstrap.servers': bootstrap_servers,
    'client.id': 'binance-producer'
})


def delivery_report(err, msg):
    if err is not None:
        print(f'Échec de la livraison du message : {err}')
    else:
        print(f'Message livré à {msg.topic()} [{msg.partition()}]')


# Récupération des données en temps réel depuis Binance et publication dans Kafka
def fetch_and_publish(symbol):
    while True:
        try:
            klines = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE)
            print("TEST OK " + str(symbol))
            for kline in klines:
                # Publier chaque kline dans le topic Kafka
                print(kline)
                producer.produce(topic_name, json.dumps(kline).encode('utf-8'), callback=delivery_report)
            producer.flush()
        except Exception as e:
            print(f"Erreur lors de la récupération des données depuis Binance : {e}")


# Appel de la fonction pour récupérer et publier les données pour un symbole spécifique (par exemple, 'BTCUSDT')
fetch_and_publish('ETHBTC')
