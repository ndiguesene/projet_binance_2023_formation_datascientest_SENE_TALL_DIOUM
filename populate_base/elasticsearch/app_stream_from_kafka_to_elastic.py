import json
import time

from binance.client import Client
from confluent_kafka import Producer
from elasticsearch import Elasticsearch

# Initialisation du client Binance
client = Client("api_key", "api_secret")

# Initialisation du producteur Kafka
producer = Producer({'bootstrap.servers': 'localhost:9092'})

# Initialisation d'Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# Liste des symboles à surveiller
symbols = client.get_all_tickers()

# Boucle pour récupérer les données pour chaque symbole
for symbol in symbols:
    kline = client.get_klines(symbol=symbol['symbol'], interval=Client.KLINE_INTERVAL_1HOUR)

    # Envoi des données à Kafka
    producer.produce('binance_data', key=symbol['symbol'], value=json.dumps(kline))
    producer.flush()

    # Stockage dans Elasticsearch
    for data in kline:
        es.index(index='binance_data', body={
            'symbol': symbol['symbol'],
            'open_time': data[0],
            'open': data[1],
            'high': data[2],
            'low': data[3],
            'close': data[4],
            'volume': data[5],
            # ... ajoutez d'autres champs ici ...
        })

    time.sleep(1)  # Pour éviter les limites d'appel de l'API Binance

# Fermer les connexions
producer.close()
es.close()
