# installation du package python-binance
# pip3 install python-binance

from binance.client import Client

from constant import api_key, api_secret, BDNAME_MYSQL, TABLENAME_MYSQL, USER_MYSQL, PASSWORD_MYSQL, HOST_MYSQL, \
    PORT_MYSQL

# init
# api_key = '7FipgVGJTbxWEyeyI5wNRyKuQwXXJcRIJBZvvQAxRY1aScVExHzdyQFMh3bLLPT5'
# api_secret = 'tnlNDg4WOt0xungysd7fAZAVKyBqqOzcgQW8MYebVo1piJzfeUC1mYkcDgJSm4T1'

client = Client(api_key=api_key, api_secret=api_secret, testnet=True)

print("DROP TABLE IF EXISTS {}.{}".format(BDNAME_MYSQL, TABLENAME_MYSQL))
print(HOST_MYSQL)

data = []
for marche in client.get_all_tickers():
    data.append(tuple(client.get_ticker(symbol=marche.get("symbol")).values()))

import mysql.connector
from mysql.connector import Error

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
        # cursor.execute("CREATE DATABASE cryptobot")
        cursor.execute("DROP TABLE IF EXISTS {}.{}".format(BDNAME_MYSQL, TABLENAME_MYSQL))
        cursor.execute(
            "CREATE TABLE {}.{} (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, date_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, "
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
            "count INT)".format(BDNAME_MYSQL, TABLENAME_MYSQL))

        # cursor.execute("select *from cryptobot.botmarche")

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
