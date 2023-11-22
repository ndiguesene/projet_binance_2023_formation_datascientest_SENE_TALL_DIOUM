# installation du package python-binance
# pip install python-binance
from elasticsearch import Elasticsearch

from constant import URL_ELASTIC, INDEX_ELASTIC, get_historic_by_symbol

data = get_historic_by_symbol(0)
print("Données finales")
print(data)
es = Elasticsearch(URL_ELASTIC)

# print(es.info())

# print(es.indices.(index='test-index', ignore=[400, 404]).body)
# print(es.indices.delete(index='reviews_new', ignore=[400, 404]).body)
print(es.index(index=INDEX_ELASTIC, document=data).body)
print(es.indices.get(index="*"))
print("OK.")
