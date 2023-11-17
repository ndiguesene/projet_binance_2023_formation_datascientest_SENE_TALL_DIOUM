# installation du package python-binance
# pip3 install python-binance

import mysql.connector
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


data = get_all_marche_statistic(client)

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
        cursor.execute("DROP DATABASE {}".format(BDNAME_MYSQL))
        cursor.execute("CREATE DATABASE {}".format(BDNAME_MYSQL))
        cursor.execute("DROP TABLE IF EXISTS {}.{}".format(BDNAME_MYSQL, TABLENAME_MYSQL))
        cursor.execute(
            "CREATE TABLE cryptobot.botmarche (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, date_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, "
            "symbol VARCHAR(50), "
            "priceChange FLOAT, "
            "priceChangePercent FLOAT, "
            "weightedAvgPrice FLOAT, "
            "prevClosePrice FLOAT, "
            "lastPrice FLOAT, "
            "lastQty FLOAT, "
            "bidPrice FLOAT, "
            "bidQty FLOAT, "
            "askPrice FLOAT, "
            "askQty FLOAT, "
            "openPrice FLOAT, "
            "highPrice FLOAT, "
            "lowPrice FLOAT, "
            "volume FLOAT, "
            "quoteVolume FLOAT, "
            "openTime FLOAT, "
            "closeTime FLOAT, "
            "firstId INT, "
            "lastId INT, "
            "count INT)")

        sql = """INSERT INTO {}.{}(symbol, priceChange, priceChangePercent, weightedAvgPrice, prevClosePrice,""" \
              """lastPrice, lastQty, bidPrice, bidQty, askPrice, askQty, openPrice, highPrice, lowPrice, volume, quoteVolume, openTime,""" \
              """closeTime, firstId, lastId, count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(
            BDNAME_MYSQL, TABLENAME_MYSQL)

        cursor.executemany(sql, data)
        # commit the transaction
        connection.commit()
    print("You're connected to database: ")
except Error as e:
    print("Error while connecting to MySQL", e)
    connection.rollback()
finally:
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")
