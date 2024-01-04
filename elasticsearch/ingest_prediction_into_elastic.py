import os
import time

import requests
from elasticsearch import Elasticsearch

from constant import predict

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
                    # client_es = Elasticsearch(hosts=[url, 'http://elasticsearch:9200/'], verify_certs=False)
                    client_es = Elasticsearch(hosts=[url], verify_certs=False)
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
# client = Client(api_key, api_secret)

# Nom de l'index Elasticsearch pour les données Binance
index_name = 'cryptobot'

data = predict()
es.index(index=index_name, body=data)
