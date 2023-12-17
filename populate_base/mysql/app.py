# installation du package python-binance
# pip3 install python-binance
import datetime
import os

import mysql.connector
from binance.client import Client

api_key = os.getenv("api_key")
api_secret = os.getenv("api_secret")
BDNAME_MYSQL = os.getenv("MYSQL_DATABASE")
TABLENAME_MYSQL = os.getenv("MYSQL_TABLENAME")
USER_MYSQL = os.getenv("MYSQL_USER")
PASSWORD_MYSQL = os.getenv("MYSQL_PASSWORD")
HOST_MYSQL = os.getenv("MYSQL_HOST")
PORT_MYSQL = os.getenv("MYSQL_PORT")

client = Client(api_key=api_key, api_secret=api_secret, testnet=True)


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


def check_mysql_connection_and_get_current_connexion():
    max_attempts = 30
    attempts = 0
    connected = False
    # Cette partie permet d'etre sur que le mysql est ready, parce que
    # Docker ne garantit pas nécessairement l'ordre de démarrage des services, ce qui peut entraîner le démarrage de votre service Python (app) avant que le service de la base de données MySQL (db)
    # ne soit prêt
    import time
    connection = None

    while not connected and attempts < max_attempts:
        try:
            connection = mysql.connector.connect(host=HOST_MYSQL,
                                                 port=PORT_MYSQL,
                                                 database=BDNAME_MYSQL,
                                                 user=USER_MYSQL,
                                                 password=PASSWORD_MYSQL)
            connected = True
            connection.close()
            print("MySQL is ready!")
        except mysql.connector.Error as err:
            print(f"Attempt {attempts + 1}: MySQL is not ready yet - Error: {err}")
            attempts += 1
            time.sleep(10)

    if not connected:
        print("Failed to connect to MySQL.")

    return connection


end_date = datetime.datetime.now()
# On prends une historique de données de 60 jours glissants
start_date = end_date - datetime.timedelta(days=60)  # 60 days ago

# Convert dates to milliseconds (required by Binance API)
start_timestamp = int(start_date.timestamp() * 1000)
end_timestamp = int(end_date.timestamp() * 1000)

data = []
print("LOG TO GET ALL MARCHES")
# allSymbols = get_all_symbols(client)
allSymbols = ["ETHBTC"]
print("nombre de marches " + str(len(allSymbols)))
# Fetch historical prices using Binance API
for symbol in allSymbols:
    print(symbol)
    historical_prices = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, start_timestamp, end_timestamp)
    # :return: list of OHLCV values (Open time, Open, High, Low, Close, Volume, Close time, Quote asset volume, Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore)
    for price_data in historical_prices:
        timestampOpen = datetime.datetime.utcfromtimestamp(price_data[0] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        timestampClose = datetime.datetime.utcfromtimestamp(price_data[6] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        price_data.pop(0)
        price_data.pop(5)
        price_data = price_data[:-3]
        price_data.extend([timestampOpen, timestampClose, symbol])  # Ajouter les 3 éléments parsed
        data.append(price_data)

print("sorti de boucle")
connection = check_mysql_connection_and_get_current_connexion()

if connection.is_connected():
    db_Info = connection.get_server_info()
    print("Connected to MySQL Server version ", db_Info)
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(BDNAME_MYSQL))
    cursor.execute("DROP TABLE IF EXISTS {}.{}".format(BDNAME_MYSQL, TABLENAME_MYSQL))
    cursor.execute(
        "CREATE TABLE " + str(BDNAME_MYSQL) + "." + str(
            TABLENAME_MYSQL) + " (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
                               "open_price FLOAT, "
                               "high_price FLOAT, "
                               "low_price FLOAT, "
                               "close_price FLOAT, "
                               "volume FLOAT, "
                               "quote_asset_volume FLOAT, "
                               "number_of_trades INT, "
                               "kline_open_time_parsed DATETIME,"
                               "kline_close_time_parsed DATETIME,"
                               "symbol VARCHAR(20))")
    print("ok")

    sql = """INSERT INTO {}.{}(open_price, high_price, low_price,close_price,""" \
          """volume, quote_asset_volume, number_of_trades, """ \
          """kline_open_time_parsed, kline_close_time_parsed, symbol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(
        BDNAME_MYSQL, TABLENAME_MYSQL)

    cursor.executemany(sql, data)
    connection.commit()
    print("MySQL connection is closed")
