import os

from fastapi import FastAPI
from pydantic import BaseModel

from constant import BDNAME_MYSQL, TABLENAME_MYSQL, getConnexionMysql

app = FastAPI(title='My API Model')

mydb = getConnexionMysql()

api_key = os.getenv("api_key")
api_secret = os.getenv("api_secret")


class MarcheModelSchema(BaseModel):
    open_price: float
    high_price: float
    low_price: float
    volume: float
    moyennemobile10: int
    timestamp: str


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


@app.get("/status")
async def checkStatus():
    return {"status": "OK"}


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

# if __name__ == "__main__":
#     uvicorn.run("app_api:app", host="127.0.0.1", port=8000, log_level="info")
