from flask import Flask

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

# app = FastAPI(
#     title='Projet OPA Crypto API',
#     description=description,
#     version="0.0.1",
#     contact={}
# )
app = Flask(__name__)


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


######
## Database info
########
mydb = mysql.connector.connect(host=HOST_MYSQL,
                               port=PORT_MYSQL,
                               database=BDNAME_MYSQL,
                               user=USER_MYSQL,
                               password=PASSWORD_MYSQL)

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
def root():
    return ResponseModel("message", "Hello World")


# @validate
# Get all marches
@app.get("/marches")
def get_marches():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM {}.{}".format(BDNAME_MYSQL, TABLENAME_MYSQL))
    result = cursor.fetchall()
    return ResponseModel(result, "All marches received.")


# Get an marche by symbol
@app.get("/marche/{symbol}")
def get_marche(symbol: str):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM {}.{} WHERE symbol = '{}'".format(BDNAME_MYSQL, TABLENAME_MYSQL, symbol))
    result = cursor.fetchone()
    return ResponseModel(result, f"symbol = {symbol} received.")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
