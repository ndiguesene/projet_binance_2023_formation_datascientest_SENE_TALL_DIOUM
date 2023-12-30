import datetime
import os

from binance.client import Client
from elasticsearch import Elasticsearch

# Configuration de l'API Binance en récuparant les variables d'enrivonnement
api_key = os.getenv("api_key")
api_secret = os.getenv("api_secret")
URL_ELASTIC = os.getenv("URL_ELASTIC")

print(api_key)
print(api_secret)
print(URL_ELASTIC)

# api_key = '7FipgVGJTbxWEyeyI5wNRyKuQwXXJcRIJBZvvQAxRY1aScVExHzdyQFMh3bLLPT5'
# api_secret = 'tnlNDg4WOt0xungysd7fAZAVKyBqqOzcgQW8MYebVo1piJzfeUC1mYkcDgJSm4T1'

# Initialisation du client Binance
client = Client(api_key, api_secret)

# Configuration de la connexion Elasticsearch
es = Elasticsearch(hosts=['http://localhost:9200/', 'http://elasticsearch:9200/'], verify_certs=False)
# Nom de l'index Elasticsearch pour les données Binance
index_name = 'cryptobot'
# if not es.indices.exists(index=index_name):
#     es.indices.create(index=index_name)
#     print("indices créés")


# Récupération des données Kline depuis Binance pour un symbole spécifique et une intervalle de 1 heure
allSymbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "USDCUSDT", "BNBUSDT"]
# allSymbols = get_all_symbols(client)
# klines = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR)

print(allSymbols)
# id,open_price,high_price,low_price,close_price,volume,quote_asset_volume,number_of_trades,kline_open_time_parsed,kline_close_time_parsed,symbol
# Transformation et indexation des données dans Elasticsearch

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
        })

    for doc in data:
        es.index(index=index_name, body=doc)
