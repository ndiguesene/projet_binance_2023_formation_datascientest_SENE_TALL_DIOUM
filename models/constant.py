<<<<<<< HEAD:models/constant.py
=======
# Parametres externalisés
import datetime

from binance import Client

api_key = '7FipgVGJTbxWEyeyI5wNRyKuQwXXJcRIJBZvvQAxRY1aScVExHzdyQFMh3bLLPT5'
api_secret = 'tnlNDg4WOt0xungysd7fAZAVKyBqqOzcgQW8MYebVo1piJzfeUC1mYkcDgJSm4T1'

>>>>>>> main:constant.py
# ELASTIC
# URL_ELASTIC = "http://54.195.84.110:9200"
URL_ELASTIC = "http://54.195.84.110:9200"
INDEX_ELASTIC = "cryptobot"

# MYSQL
# HOST_MYSQL = "63.32.7.247"
HOST_MYSQL = "db"
PORT_MYSQL = "3306"
BDNAME_MYSQL = "cryptobot"
TABLENAME_MYSQL = "botmarche"
USER_MYSQL = "root"
<<<<<<< HEAD:models/constant.py
PASSWORD_MYSQL = "root"
=======
PASSWORD_MYSQL = "Password"

client = Client(api_key=api_key, api_secret=api_secret, testnet=True)


def get_data_historical_from_csv_file(fileName):
    import pandas as pd
    df = pd.read_csv(fileName)
    return df


def get_data_from_marche(client, marche):
    return tuple(client.get_ticker(symbol=marche).values())


def get_all_marche_statistic(client):
    data = []
    for marche in client.get_all_tickers():
        data.append(get_data_from_marche(client=client, marche=marche.get("symbol")))
    return data


def get_all_symbols(client):
    data = []
    for marche in client.get_all_tickers():
        data.append(marche.get("symbol"))
    return data


def get_historic_by_symbol(countDays):
    end_date = datetime.datetime.now()
    # On prends une historique de données de 90 jours glissants
    start_date = end_date - datetime.timedelta(days=countDays)  # 90 days ago

    # Convert dates to milliseconds (required by Binance API)
    start_timestamp = int(start_date.timestamp() * 1000)
    end_timestamp = int(end_date.timestamp() * 1000)

    data = []
    i = 0
    allSymbols = get_all_symbols(client=client)
    # Fetch historical prices using Binance API
    for symbol in allSymbols:
        historical_prices = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, start_timestamp,
                                                         end_timestamp)
        # Process the data (print or save it as needed)
        for price_data in historical_prices:
            timestampOpen = datetime.datetime.utcfromtimestamp(price_data[0] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            timestampClose = datetime.datetime.utcfromtimestamp(price_data[6] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            price_data.append(timestampOpen)  # La date
            price_data.append(timestampClose)  # La date
            price_data.append(symbol)  # La date du
            data.append(price_data)
    return data
>>>>>>> main:constant.py
