import pickle
import random
from typing import Literal

import models.ml.modeler as mdl
import numpy as np
import pandas as pd
import requests
from fastapi import FastAPI, Request
from fastapi import Security, Depends, FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.security.api_key import APIKeyHeader, APIKey
from joblib import load
from pydantic import BaseModel
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.metrics import balanced_accuracy_score
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import RobustScaler
from werkzeug.exceptions import NotFound, Unauthorized, BadRequest

description = """
This API lets you get infarctus score for a given patient.
The api access is restricted.

## Scores
* /predict/v1 let you **get scores for new patients using a logistic regression method**.
* /predict/v2 let you **get scores for new patients using a random forest method**.

## Models
You will be able to:
* **Train a new model from new data using a logistic regression model**.
* **Train a new model from new data using a random forrst model**.

"""

PROJET2_API_KEY = "OTS7KgBNNBYORI7nVjQeJA"
API_KEY_NAME = "project2_access_token"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def get_models():
    """
    load the models from disk
    and create a dictionary to hold
    Returns:
    dict: loaded models
    """
    models = {
        "model_lr": load("./stroke_model_lr.joblib"),
        "model_rf": load("./stroke_model_rf.joblib")
    }
    return models


# load models from disk
models = get_models()

api = FastAPI(
    title='Projet 2 API',
    description=description,
    version="0.0.1",
    contact={
    }
)


class Patient(BaseModel):
    gender: Literal['Male', 'Female']
    age: float
    hypertension: Literal[1, 0]
    heart_disease: Literal[1, 0]
    ever_married: Literal['Yes', 'No']
    work_type: Literal['Private', 'Self-employed', 'children', 'Govt_job', 'Never_worked']
    residence_type: Literal['Urban', 'Rural']
    avg_glucose_level: float
    bmi: float
    smoking_status: Literal['never smoked', 'Unknown', 'formerly smoked', 'smokes']


class Model(BaseModel):
    url: str
    kind: Literal["lr", "rf"]


async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == PROJET2_API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate X-token header"
    )


@api.post("/models/train")
def train_with_new_data(model: Model, request: Request, api_key_header: APIKey = Depends(get_api_key)):
    print("Kind ", model.kind, model.kind == "lr")
    if model.kind == "lr":
        try:
            mdl.create_logistic_regression_model(model.url)
            return {"status": "OK"}
        except Exception:
            raise HTTPException(
                status_code="405",
                detail="An error occured"
            )
    else:
        try:
            mdl.create_random_forest_model(model.url)
            return {"status": "OK"}
        except Exception:
            raise HTTPException(
                status_code="405",
                detail="An error occured"
            )


@api.post("/predict/v1")
async def predict_lr_score(patient: Patient, request: Request, api_key_header: APIKey = Depends(get_api_key)):
    data = [[patient.gender, patient.age, patient.hypertension, patient.heart_disease, patient.ever_married,
             patient.work_type, patient.residence_type, patient.avg_glucose_level, patient.bmi, patient.smoking_status]]

    model_lr = models['model_lr']

    X = pd.DataFrame(data, columns=['gender', 'age', 'hypertension', 'heart_disease', 'ever_married', 'work_type',
                                    'Residence_type', 'avg_glucose_level', 'bmi', 'smoking_status'])

    score = model_lr.predict(X).tolist()

    proba = model_lr.predict_proba(X).tolist()

    log_proba = model_lr.predict_log_proba(X).tolist()

    return {"score": score,
            "proba": proba,
            "log_proba": log_proba
            }


@api.post("/predict/v2")
async def predict_rf_score(patient: Patient, request: Request, api_key_header: APIKey = Depends(get_api_key)):
    data = [[patient.gender, patient.age, patient.hypertension, patient.heart_disease, patient.ever_married,
             patient.work_type, patient.residence_type, patient.avg_glucose_level, patient.bmi, patient.smoking_status]]

    model_rf = models['model_rf']

    X = pd.DataFrame(data, columns=['gender', 'age', 'hypertension', 'heart_disease', 'ever_married', 'work_type',
                                    'Residence_type', 'avg_glucose_level', 'bmi', 'smoking_status'])

    score = model_rf.predict(X).tolist()

    proba = model_rf.predict_proba(X).tolist()

    log_proba = model_rf.predict_log_proba(X).tolist()

    return {"score": score,
            "proba": proba,
            "log_proba": log_proba
            }
