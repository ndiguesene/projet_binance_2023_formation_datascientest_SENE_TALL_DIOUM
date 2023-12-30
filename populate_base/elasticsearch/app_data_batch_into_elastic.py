import datetime
import os
import time

import requests
from binance.client import Client
from elasticsearch import Elasticsearch

# Configuration de l'API Binance en récuparant les variables d'enrivonnement
api_key = os.getenv("api_key")
api_secret = os.getenv("api_secret")
URL_ELASTIC = os.getenv("URL_ELASTIC")


def check_elasticsearch_instance(url):
    client_es = None
    connected = False
    max_attempts = 30
    attempts = 0
    while not connected and attempts < max_attempts:
        try:
            # Effectuer une requête GET à l'URL de santé Elasticsearch
            response = requests.get(url + "_cluster/health")

            # Vérifier si la requête a réussi (code de statut 200)
            if response.status_code == 200:
                health_data = response.json()
                # # Vérifier l'état de santé (par exemple, si l'état est 'green')
                if health_data['status'] == 'green':
                    client_es = Elasticsearch(hosts=[url, 'http://elasticsearch:9200/'], verify_certs=False)
                    connected = True
                    print("Elasticsearch is healthy GREEN !")
                else:
                    print(f"Elasticsearch status: {health_data['status']}")
            else:
                print(f"Failed to fetch Elasticsearch health. Status code: {response.status_code}")
            attempts += 1
            # Attendre pendant 10 secondes avant de vérifier à nouveau
            time.sleep(10)
        except requests.RequestException as e:
            print(f"Request Exception: {e}")
    return client_es


# api_key = '7FipgVGJTbxWEyeyI5wNRyKuQwXXJcRIJBZvvQAxRY1aScVExHzdyQFMh3bLLPT5'
# api_secret = 'tnlNDg4WOt0xungysd7fAZAVKyBqqOzcgQW8MYebVo1piJzfeUC1mYkcDgJSm4T1'
# URL_ELASTIC = 'http://localhost:9200/'

# Configuration de la connexion Elasticsearch
es = check_elasticsearch_instance(URL_ELASTIC)
# Initialisation du client Binance
client = Client(api_key, api_secret)

# Nom de l'index Elasticsearch pour les données Binance
index_name = 'cryptobot'

# Récupération des données Kline depuis Binance pour un symbole spécifique et une intervalle de 1 heure
allSymbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "USDCUSDT", "BNBUSDT"]
# allSymbols = get_all_symbols(client)

print(allSymbols)
for symbol in allSymbols:
    klines = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR)
    data = []
    # :return: list of OHLCV values (Open time, Open, High, Low, Close, Volume, Close time, Quote asset volume, Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore)
    for kline in klines:
        data.append({
            'symbol': symbol,
            'open_time': datetime.datetime.utcfromtimestamp(kline[0] / 1000).strftime('%Y-%m-%d %H:%M:%S'),
            'open_price': float(kline[1]),
            'high_price': float(kline[2]),
            'low_price': float(kline[3]),
            'close_price': float(kline[4]),
            'volume': float(kline[5]),
            'close_time': datetime.datetime.utcfromtimestamp(kline[6] / 1000).strftime('%Y-%m-%d %H:%M:%S'),
            'quote_asset_volume': float(kline[7]),
            'number_of_trades': int(kline[8]),
            'is_closed': bool(kline[9])
        })

    for doc in data:
        es.index(index=index_name, body=doc)
