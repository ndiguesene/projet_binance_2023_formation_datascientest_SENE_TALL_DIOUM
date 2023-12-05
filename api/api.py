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
