import os

import numpy as np
import pandas as pd
from binance.client import Client
from fastapi import HTTPException, FastAPI
from joblib import load
from pydantic import BaseModel
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

import app as mdl
from constant import BDNAME_MYSQL, TABLENAME_MYSQL


def get_models(model_name, symbol):
    home_path = os.getcwd()
    models = {
        "model_svm": load(home_path + "/opa_cypto_" + model_name + "_" + symbol + ".joblib"),
        "model_xgb": load(home_path + "/opa_cypto_" + model_name + "_" + symbol + ".joblib"),
        "model_rf": load(home_path + "/opa_cypto_" + model_name + "_" + symbol + ".joblib"),
        "model_lr": load(home_path + "/opa_cypto_" + model_name + "_" + symbol + ".joblib"),
        "model_gb": load(home_path + "/opa_cypto_" + model_name + "_" + symbol + ".joblib")
    }
    return models


# app = Flask(__name__)
app = FastAPI(title='My API Model')

mydb = mdl.getConnexionMysql()

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


@app.get("/models/train")
async def train_with_new_data():
    try:
        result = mdl.create_all_models()
        return result
    except Exception:
        raise HTTPException(status_code="405", detail="An error occured")


@app.get("/predict/v1")
async def predict_rf_score():
    symbols_to_filter = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "USDCUSDT", "BNBUSDT"]
    data = []
    for symbol in symbols_to_filter:
        client = Client(api_key=api_key, api_secret=api_secret, testnet=True)
        klines = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR)
        columns = ['open_time', 'open_price', 'high_price', 'low_price', 'close_price', 'volume', 'close_time',
                   'quote_asset_volume',
                   'number_of_trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore']
        df = pd.DataFrame(klines, columns=columns)
        df.loc[:, 'symbol'] = symbol
        selected_columns = ['open_price', 'high_price', 'low_price', 'close_price', 'volume', 'quote_asset_volume',
                            'number_of_trades', 'open_time', 'close_time', 'symbol']
        df = df[selected_columns]
        df.sort_values(by=['symbol', 'open_time'], inplace=True)

        # Création des indicateurs métiers
        df['volume'] = df['volume'].astype(float)
        df['open_price'] = df['open_price'].astype(float)
        df['close_price'] = df['close_price'].astype(float)

        df['cumulative_volume'] = df.groupby('symbol')['volume'].cumsum()
        df['price_range'] = df['close_price'] - df['open_price']
        df['rolling_mean'] = df.groupby('symbol')['close_price'].rolling(window=10).mean().reset_index(level=0,
                                                                                                       drop=True)
        df['rolling_mean'].fillna(df['close_price'], inplace=True)

        # Création de la variable cible
        condition_achat = (
                (df['price_range'] > 0) &
                (df['price_range'].shift(1) > 0) &
                (df['close_price'] > df['close_price'].shift(1))
        )

        condition_vente = (
                (df['close_price'] < df['rolling_mean']) &
                (df['cumulative_volume'].shift(1) < df['cumulative_volume'])
        )

        df['achat_vente'] = np.where(condition_achat, 1, np.where(condition_vente, 2, 0))

        # Création d'une variable qui tient compte de la temporalité
        df['action_jour_precedent'] = df.groupby('symbol')['achat_vente'].shift(1)
        df['action_jour_precedent'] = df['action_jour_precedent'].fillna(0).astype(int)

        # Encodage des variables temporelles
        df['open_time'] = pd.to_datetime(df['open_time'])
        df['close_time'] = pd.to_datetime(df['close_time'])
        df['hour'] = df['open_time'].dt.hour
        df['day_of_week'] = df['open_time'].dt.dayofweek
        df['month'] = df['open_time'].dt.month
        df.sort_values(by=['symbol', 'open_time'], inplace=True)
        df = df.drop(['open_time', 'close_time', 'high_price', 'low_price', 'achat_vente'], axis=1)

        df = pd.get_dummies(df, columns=['hour', 'day_of_week', 'month'])
        # Format input données
        # 'open_price', 'close_price', 'volume', 'quote_asset_volume',
        # 'number_of_trades', 'symbol', 'cumulative_volume', 'price_range',
        # 'rolling_mean', 'action_jour_precedent', 'hour_0', 'day_of_week_3','month_1'
        X = preprocess_data(df)

        # load models from disk
        models = get_models(model_name='XGBoost', symbol=symbol)
        model_rf = models['model_xgb']

        prediction = model_rf.predict(X).tolist()
        data.append({"prediction": prediction, "symbol": symbol})
    return data


def preprocess_data(X_train):
    # Encoding de la colonne 'symbol' avec LabelEncoder
    label_encoder = LabelEncoder()
    X_train['symbol'] = label_encoder.fit_transform(X_train['symbol'])

    # Normalisation des colonnes sélectionnées avec MinMaxScaler
    columns_to_normalize = ['open_price', 'close_price', 'volume', 'quote_asset_volume', 'number_of_trades',
                            'cumulative_volume', 'price_range', 'rolling_mean']
    min_max_scaler = MinMaxScaler()
    X_train[columns_to_normalize] = min_max_scaler.fit_transform(X_train[columns_to_normalize])

    return X_train

# if __name__ == "__main__":
#     uvicorn.run("server:app", host="127.0.0.1", port=9000, log_level="info")
