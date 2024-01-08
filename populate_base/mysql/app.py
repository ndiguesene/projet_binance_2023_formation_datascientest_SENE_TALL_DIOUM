import datetime
import os

import mysql.connector
import pandas as pd
from binance.client import Client

api_key = os.getenv("api_key")
api_secret = os.getenv("api_secret")

BDNAME_MYSQL = os.getenv("MYSQL_DATABASE")
TABLENAME_MYSQL = os.getenv("MYSQL_TABLENAME")
USER_MYSQL = os.getenv("MYSQL_USER")
PASSWORD_MYSQL = os.getenv("MYSQL_PASSWORD")
HOST_MYSQL = os.getenv("MYSQL_HOST")
PORT_MYSQL = os.getenv("MYSQL_PORT")

# HOST_MYSQL = 'localhost'
# BDNAME_MYSQL = 'cryptobot'
# USER_MYSQL = 'root'
# PASSWORD_MYSQL = 'Password'
# PORT_MYSQL = "3306"
# # PASSWORD_MYSQL = 'root'
# TABLENAME_MYSQL = "botmarche"
# api_key = '7FipgVGJTbxWEyeyI5wNRyKuQwXXJcRIJBZvvQAxRY1aScVExHzdyQFMh3bLLPT5'
# api_secret = 'tnlNDg4WOt0xungysd7fAZAVKyBqqOzcgQW8MYebVo1piJzfeUC1mYkcDgJSm4T1'

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
    # Docker ne garantit pas nécessairement l'ordre de démarrage des services, ce qui peut entraîner le démarrage de votre service Python (app)
    # avant que le service de la base de données MySQL (db)
    # ne soit prêt
    import time
    connection_return = None
    while not connected and attempts < max_attempts:
        try:
            print(f"Attempting to connect to MySQL: attempt {attempts + 1}")
            connection_return = mysql.connector.connect(host=HOST_MYSQL,
                                                        port=PORT_MYSQL,
                                                        database=BDNAME_MYSQL,
                                                        user=USER_MYSQL,
                                                        password=PASSWORD_MYSQL)
            connected = True
            print("MySQL is ready!")
        except mysql.connector.Error as err:
            print(f"Attempt {attempts + 1}: MySQL is not ready yet - Error: {err}")
            attempts += 1
            time.sleep(10)

    return connection_return


connection = check_mysql_connection_and_get_current_connexion()
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
                           "open_time double, "
                           "kline_open_time_parsed DATETIME,"
                           "close_time double,"
                           "kline_close_time_parsed DATETIME,"
                           "symbol VARCHAR(15))")

end_date = datetime.datetime.now()
# On prends une historique de données de 60 jours glissants
start_date = end_date - datetime.timedelta(days=30)  # 30 days ago

# Convert dates to milliseconds (required by Binance API)
start_timestamp = int(start_date.timestamp() * 1000)
end_timestamp = int(end_date.timestamp() * 1000)

print("LOG TO GET ALL MARCHES")
allSymbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "USDCUSDT", "BNBUSDT"]
columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume',
           'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore']
# Fetch historical prices using Binance API
for symbol in allSymbols:
    print(symbol)
    historical_prices = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, start_timestamp,
                                                     end_timestamp)
    df = pd.DataFrame(historical_prices, columns=columns)
    # Select specific columns
    selected_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Quote Asset Volume', 'Number of Trades', 'Open Time',
                        'kline_open_time_parsed',
                        'Close Time', 'kline_close_time_parsed', 'Symbol']
    df.loc[:, 'Symbol'] = symbol
    df['kline_open_time_parsed'] = df['Open Time'].apply(
        lambda x: datetime.datetime.fromtimestamp(x / 1000).strftime('%Y-%m-%d %H:%M:%S'))
    df['kline_close_time_parsed'] = df['Close Time'].apply(
        lambda x: datetime.datetime.fromtimestamp(x / 1000).strftime('%Y-%m-%d %H:%M:%S'))

    selected_df = df[selected_columns]
    data = [tuple(row) for row in selected_df.to_numpy()]
    sql = """INSERT INTO {}.{}(open_price, high_price, low_price,close_price,""" \
          """volume, quote_asset_volume, number_of_trades, """ \
          """open_time, kline_open_time_parsed, close_time, kline_close_time_parsed, symbol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(
        BDNAME_MYSQL, TABLENAME_MYSQL)

    cursor.executemany(sql, data)
    connection.commit()

print("MySQL connection is closed")
