import os

import pandas as pd
from fastapi import HTTPException, FastAPI, Request
from fastapi.encoders import jsonable_encoder
from joblib import load
from pydantic import BaseModel

import app as mdl
from constant import BDNAME_MYSQL, TABLENAME_MYSQL


def get_models():
    home_path = os.getcwd()
    models = {
        "model_rf": load(home_path + "/opa_cypto_model_rf.joblib")
    }
    return models


# app = Flask(__name__)
app = FastAPI(title='My API Model')

mydb = mdl.getConnexionMysql()


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


@app.get("/models/train")
async def train_with_new_data():
    try:
        scrore = mdl.create_random_forest_model()
        return scrore
    except Exception:
        raise HTTPException(status_code="405", detail="An error occured")


@app.post("/predict/v1")
async def predict_rf_score(symbol: MarcheModelSchema, request: Request):
    # format data
    #     "open_price": 0.1615,
    #     "high_price": 0.1686,
    #     "low_price": 0.161,
    #     "timestamp": "2023-12-28 13:00:00",
    #     "volume": 3.20295,
    #     "moyennemobile10": 1 => data['moyennemobile10'] = data['close_price'].rolling(window=10).mean()
    # Ici on doit consommer directement les données qui viennent de ElasticSeach

    # mydata = request.get_json()
    # print("1")
    # print(mydata)
    mydata = jsonable_encoder(symbol)
    # load models from disk
    models = get_models()
    model_rf = models['model_rf']
    X = pd.DataFrame(mydata, index=["timestamp"])
    X['timestamp'] = pd.to_datetime(X['timestamp']).astype(int) / 10 ** 9
    # X['timestamp'] = pd.to_datetime(X['timestamp'])

    prediction = model_rf.predict(X).tolist()
    # proba = model_rf.predict_proba(X).tolist()
    # log_proba = model_rf.predict_log_proba(X).tolist()
    return {"prediction": prediction, "data": mydata}
