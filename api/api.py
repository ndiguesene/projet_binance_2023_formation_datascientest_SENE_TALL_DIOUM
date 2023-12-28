from fastapi import FastAPI

description = """ This API helps you query data from a MySQL database.
The data are available from the Binance API

## Queries
* Get marche from the table
* Save a new marche crypto bot in the table
"""

import mysql.connector
from pydantic import BaseModel

from constant import BDNAME_MYSQL, TABLENAME_MYSQL, USER_MYSQL, PASSWORD_MYSQL, \
    HOST_MYSQL, \
    PORT_MYSQL

app = FastAPI(title='My API Data From MYSQL')


class MarcheSchema(BaseModel):
    id: int
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int
    quote_asset_volume: float
    number_of_trades: int
    kline_open_time_parsed: str
    kline_close_time_parsed: str
    symbol: str


def symbol_helper(symbol) -> dict:
    return {
        "id": str(symbol[0]),
        "open_price": float(symbol[1]),
        "high_price": float(symbol[2]),
        "low_price": float(symbol[3]),
        "close_price": float(symbol[4]),
        "volume": float(symbol[5]),
        "quote_asset_volume": str(symbol[6]),
        "number_of_trades": str(symbol[7]),
        "kline_open_time_parsed": str(symbol[8]),
        "kline_close_time_parsed": str(symbol[9]),
        "symbol": str(symbol[10])
    }


max_attempts = 30
attempts = 0
connected = False
# Cette partie permet d'etre sur que le mysql est ready, parce que
# Docker ne garantit pas nécessairement l'ordre de démarrage des services, ce qui peut entraîner le démarrage de votre service Python (app)
# avant que le service de la base de données MySQL (db) ne soit prêt
import time

mydb = None

while not connected and attempts < max_attempts:
    try:
        mydb = mysql.connector.connect(host=HOST_MYSQL,
                                       port=PORT_MYSQL,
                                       database=BDNAME_MYSQL,
                                       user=USER_MYSQL,
                                       password=PASSWORD_MYSQL)
        connected = True
        # connection.close()
        print("MySQL is ready!")
    except mysql.connector.Error as err:
        print(f"Attempt {attempts + 1}: MySQL is not ready yet - Error: {err}")
        attempts += 1
        time.sleep(10)


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}


@app.get("/")
async def root():
    return ResponseModel("message", "Hello World")


# @validate
# Get all marches
@app.get("/symbols")
async def get_marches():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM {}.{}".format(BDNAME_MYSQL, TABLENAME_MYSQL))
    result = cursor.fetchall()
    data = []
    for res in result:
        data.append(symbol_helper(res))
    return ResponseModel(data, "All marches received.")


# Get an marche by symbol
@app.get("/symbol/{symbol}")
async def get_marche(symbol: str):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM {}.{} WHERE symbol = '{}'".format(BDNAME_MYSQL, TABLENAME_MYSQL, symbol))
    result = cursor.fetchall()
    data = []
    for res in result:
        data.append(symbol_helper(res))
    return ResponseModel(data, f"symbol = {symbol} received.")
