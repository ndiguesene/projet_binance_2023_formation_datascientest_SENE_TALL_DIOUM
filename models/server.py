import pandas as pd
from fastapi import HTTPException
from flask import Flask, request
from joblib import load
from pydantic import BaseModel

import models.app as mdl


def get_models():
    models = {
        "model_rf": load("./opa_cypto_model_rf.joblib")
    }
    return models


app = Flask(__name__)


class MarcheSchema(BaseModel):
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


@app.route("/status", methods=['GET', 'POST'])
def checkStatus():
    return {"status": "OK"}


@app.route("/models/train", methods=['GET'])
def train_with_new_data():
    try:
        scrore = mdl.create_random_forest_model(link="../botmarche_ok.csv")
        return scrore
    except Exception:
        raise HTTPException(status_code="405", detail="An error occured")


@app.route("/predict/v1", methods=['POST'])
def predict_rf_score():
    # format data
    #     "open_price": 0.1615,
    #     "high_price": 0.1686,
    #     "low_price": 0.161,
    #     "close_price": 0.1638,
    #     "volume": 3.20295,
    #     "moyennemobile10": 1

    mydata = request.get_json()
    # my_df = pd.DataFrame([mydata])
    # load models from disk
    models = get_models()
    model_rf = models['model_rf']
    print(type(mydata))
    print(mydata)
    X = pd.DataFrame(mydata)

    # X = pd.DataFrame(mydata,
    #                  columns=['open_price', 'high_price', 'low_price', 'close_price', 'volume', 'quote_asset_volume',
    #                           'number_of_trades', 'kline_open_time_parsed', 'kline_close_time_parsed', 'symbol'])
    # {'open_price': 0.1615, 'high_price': 0.1686, 'low_price': 0.161, 'close_price': 0.1638, 'volume': 3.20295, 'quote_asset_volume': 0.526027,
    # 'number_of_trades': 96, 'kline_open_time_parsed': '2023-11-01 00:00:00', 'kline_close_time_parsed': '2023-11-01 23:59:59', 'symbol': 'YFIBTC'}
    print(X)

    prediction = model_rf.predict(X).tolist()
    print(prediction)

    # proba = model_rf.predict_proba(X).tolist()
    # log_proba = model_rf.predict_log_proba(X).tolist()
    return {"prediction": prediction}


app.run(host="localhost", port=5000)
