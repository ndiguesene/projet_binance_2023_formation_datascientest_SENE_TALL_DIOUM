import os

import pandas as pd
from fastapi import HTTPException, FastAPI, Request
from fastapi.encoders import jsonable_encoder
from joblib import load
from pydantic import BaseModel

import app as mdl


def get_models():
    home_path = os.getcwd()
    models = {
        "model_rf": load(home_path + "/opa_cypto_model_rf.joblib")
    }
    return models


# app = Flask(__name__)
app = FastAPI(title='My API Model')


class MarcheSchema(BaseModel):
    open_price: float
    high_price: float
    low_price: float
    volume: float
    moyennemobile10: int
    timestamp: str


@app.get("/status")
async def checkStatus():
    return {"status": "OK"}


@app.get("/models/train")
async def train_with_new_data():
    try:
        scrore = mdl.create_random_forest_model()
        return scrore
    except Exception:
        raise HTTPException(status_code="405", detail="An error occured")


@app.post("/predict/v1")
async def predict_rf_score(symbol: MarcheSchema, request: Request):
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
