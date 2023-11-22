# installation du package python-binance
# pip3 install python-binance

import mysql.connector
from mysql.connector import Error

from constant import BDNAME_MYSQL, TABLENAME_MYSQL, USER_MYSQL, PASSWORD_MYSQL, HOST_MYSQL, \
    PORT_MYSQL, get_historic_by_symbol

data = get_historic_by_symbol(90)
print("Données finales")
# print(data)

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
            "CREATE TABLE cryptobot.botmarche (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, date_time_ingest DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, "
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
