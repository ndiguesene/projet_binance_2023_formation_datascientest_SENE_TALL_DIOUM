# installation du package python-binance
# pip install python-binance
from binance.client import Client
from elasticsearch import Elasticsearch

from constant import api_key, api_secret, URL_ELASTIC, INDEX_ELASTIC

client = Client(api_key=api_key, api_secret=api_secret, testnet=True)

data = []
# i = 0
for marche in client.get_all_tickers():
    data.append(tuple(client.get_ticker(symbol=marche.get("symbol")).values()))
    # Tester à indexer quelques lignes
#    if (i == 1):
#        break
#    i = i + 1

es = Elasticsearch(URL_ELASTIC)

# print(es.info())

# print(es.indices.(index='test-index', ignore=[400, 404]).body)
# print(es.indices.delete(index='reviews_new', ignore=[400, 404]).body)
print(es.index(index=INDEX_ELASTIC, document=data).body)
print(es.indices.get(index="*"))
print("OK.")
