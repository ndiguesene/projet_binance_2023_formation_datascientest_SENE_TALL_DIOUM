import json
import os

from binance.client import Client
from confluent_kafka import Producer

# Configuration de l'API Binance en récuparant les variables d'enrivonnement
api_key = os.getenv("api_key")
api_secret = os.getenv("api_secret")
bootstrap_servers = os.getenv("SERVERS")
topic_name = os.getenv("topic_name")

client = Client(api_key=api_key, api_secret=api_secret, testnet=False)

producer = Producer({
    'bootstrap.servers': bootstrap_servers,
    'client.id': 'binance-producer'
})


def get_all_symbols(client):
    data = []
    for marche in client.get_all_tickers():
        data.append(marche.get("symbol"))
    return data


def delivery_report(err, msg):
    if err is not None:
        print(f'Échec de la livraison du message : {err}')
    else:
        print(f'Message livré à {msg.topic()} [{msg.partition()}]')


# Récupération des données en temps réel depuis Binance et publication dans Kafka
def fetch_and_publish(symbols):
    while True:
        try:
            for symbol in symbols:
                klines = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR)
                for kline in klines:
                    # Publier chaque kline dans le topic Kafka
                    producer.produce(topic_name, json.dumps(kline).encode('utf-8'), callback=delivery_report)
                producer.flush()
        except Exception as e:
            print(f"Erreur lors de la récupération des données depuis Binance : {e}")


# Appel de la fonction pour récupérer et publier les données pour un symbole spécifique (par exemple, 'BTCUSDT')
allSymbols = get_all_symbols(client)
# fetch_and_publish('ETHBTC')
fetch_and_publish(allSymbols)
