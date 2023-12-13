# installation du package python-binance
# pip install python-binance
import os
import datetime
from binance.client import Client
from pyspark.streaming import StreamingContext
from elasticsearch import Elasticsearch
import requests
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from binance.client import Client
from constant import api_key, api_secret, URL_ELASTIC, INDEX_ELASTIC

os.environ["JAVA_HOME"] = "/Library/Java/JavaVirtualMachines/jdk1.8.0_202.jdk/Contents/Home"
os.environ["PYSPARK_PYTHON"] = "/usr/local/bin/python3.11"
os.environ["PYSPARK_DRIVER_PYTHON"] = "/usr/local/bin/python3.11"


def getAllMarches(client):
    client.get_all_tickers()


# Initialisation de SparkSession
spark = SparkSession.builder.appName("BinanceDataStructuredStreaming").getOrCreate()

# Définition du schéma pour les données reçues depuis l'API Binance
schema = StructType([
    StructField("open_price", StringType(), True),
    StructField("high_price", StringType(), True),
    StructField("low_price", StringType(), True),
    StructField("close_price", StringType(), True),
    StructField("volume", StringType(), True),
    StructField("quote_asset_volume", StringType(), True),
    StructField("number_of_trades", IntegerType(), True),
    StructField("kline_open_time_parsed", StringType(), True),
    StructField("kline_close_time_parsed", StringType(), True),
    StructField("symbol", StringType(), True)
])

# Configuration des informations pour Elasticsearch
es_host = URL_ELASTIC  # Remplacez-le par votre hôte Elasticsearch
es_index = INDEX_ELASTIC  # Nom de l'index Elasticsearch


# Fonction pour récupérer les données depuis l'API Binance
def get_binance_data(symbol):
    client = Client(api_key, api_secret)
    historical_klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
    data = []
    for price_data in historical_klines:
        timestampOpen = datetime.datetime.utcfromtimestamp(price_data[0] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        timestampClose = datetime.datetime.utcfromtimestamp(price_data[6] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        price_data.pop(0)
        price_data.pop(5)
        price_data = price_data[:-3]
        price_data.extend([timestampOpen, timestampClose, symbol])  # Ajouter les 3 éléments parsed
        data.append(price_data)
    return data


# [1701855720000, '43833.76000000', '43848.37000000', '43833.76000000', '43848.36000000', '13.46445000', 1701855779999, '590265.77386300', 920, '7.07177000', '310016.63954220', '0']

# Fonction pour envoyer les données à Elasticsearch
def send_to_elasticsearch(df):
    # es = Elasticsearch(es_host)
    df.write.format("org.elasticsearch.spark.sql") \
        .option("es.nodes", es_host) \
        .option("es.port", "9200") \
        .mode("append") \
        .save(es_index)

# Création du DataFrame pour Structured Streaming
symbols = ["BTCUSDT"]  # Liste des symboles à surveiller
dataframes = spark.createDataFrame([], schema)
for symbol in symbols:
    df = spark.createDataFrame(get_binance_data(symbol), schema)
    dataframes = dataframes.union(df)

# Écriture du flux en continu vers Elasticsearch
streaming_query = dataframes.writeStream \
    .outputMode("append") \
    .format("console").start()
    ##.foreachBatch(send_to_elasticsearch) \
    #.foreachBatch(df=> df.show()) \

# Attente de la terminaison du streaming
streaming_query.awaitTermination()
