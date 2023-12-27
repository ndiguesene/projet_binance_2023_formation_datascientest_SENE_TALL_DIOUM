import os

import pandas as pd
from fastapi import HTTPException
from flask import Flask, request
from joblib import load
from pydantic import BaseModel

import app as mdl


def get_models():
    home_path = os.getcwd()
    models = {
        "model_rf": load(home_path + "/opa_cypto_model_rf.joblib")
    }
    return models


app = Flask(__name__)


class MarcheSchema(BaseModel):
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: float
    moyennemobile10: int


@app.route("/status", methods=['GET', 'POST'])
def checkStatus():
    return {"status": "OK"}


@app.route("/models/train", methods=['GET'])
def train_with_new_data():
    try:
        scrore = mdl.create_random_forest_model()
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
    # load models from disk
    models = get_models()
    model_rf = models['model_rf']
    X = pd.DataFrame(mydata)

    prediction = model_rf.predict(X).tolist()
    # proba = model_rf.predict_proba(X).tolist()
    # log_proba = model_rf.predict_log_proba(X).tolist()
    return {"prediction": prediction}


app.run(host="0.0.0.0", port=9000)
