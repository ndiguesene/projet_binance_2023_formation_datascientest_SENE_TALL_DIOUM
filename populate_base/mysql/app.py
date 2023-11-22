# installation du package python-binance
# pip3 install python-binance

import mysql.connector
import datetime
from binance.client import Client
from mysql.connector import Error

from constant import api_key, api_secret, BDNAME_MYSQL, TABLENAME_MYSQL, USER_MYSQL, PASSWORD_MYSQL, HOST_MYSQL, \
    PORT_MYSQL

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


end_date = datetime.datetime.now()
# On prends une historique de données de 90 jours glissants
start_date = end_date - datetime.timedelta(days=90)  # 90 days ago

# Convert dates to milliseconds (required by Binance API)
start_timestamp = int(start_date.timestamp() * 1000)
end_timestamp = int(end_date.timestamp() * 1000)

data = []
allSymbols = get_all_symbols(client)
# Fetch historical prices using Binance API
for symbol in allSymbols:
    historical_prices = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, start_timestamp, end_timestamp)
    # Process the data (print or save it as needed)
    for price_data in historical_prices:
        timestampOpen = datetime.datetime.utcfromtimestamp(price_data[0] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        timestampClose = datetime.datetime.utcfromtimestamp(price_data[6] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        price_data.append(timestampOpen)  # La date
        price_data.append(timestampClose)  # La date
        price_data.append(symbol)  # La date du
    data.append(price_data)

# print(f"nombre de colonne = {len(data)}")
try:
    connection = mysql.connector.connect(host=HOST_MYSQL,
                                         port=PORT_MYSQL,
                                         database=BDNAME_MYSQL,
                                         user=USER_MYSQL,
                                         password=PASSWORD_MYSQL)
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(BDNAME_MYSQL))
        cursor.execute("DROP TABLE IF EXISTS {}.{}".format(BDNAME_MYSQL, TABLENAME_MYSQL))
        cursor.execute(
            "CREATE TABLE cryptobot.botmarche_new (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, date_time_ingest DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, "
            "kline_open_time VARCHAR(20), "
            "open_price FLOAT, "
            "high_price FLOAT, "
            "low_price FLOAT, "
            "close_price FLOAT, "
            "volume FLOAT, "
            "kline_close_time VARCHAR(20), "
            "quote_asset_volume FLOAT, "
            "number_of_trades INT, "
            "taker_buy_base_asset_volume FLOAT, "
            "taker_buy_quote_asset_volume FLOAT, "
            "count INT,"
            "kline_open_time_parsed DATETIME,"
            "kline_close_time_parsed DATETIME,"
            "symbol VARCHAR(20)"
            ")")

        sql = """INSERT INTO {}.{}(kline_open_time, open_price, high_price, low_price,""" \
              """close_price, volume, kline_close_time, quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume,""" \
              """count, kline_open_time_parsed, kline_close_time_parsed, symbol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(
            BDNAME_MYSQL, TABLENAME_MYSQL)

        cursor.executemany(sql, data)
        connection.commit()
    print("You're connected to database: ")
except Error as e:
    print("Error while connecting to MySQL", e)
    connection.rollback()
finally:
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")
