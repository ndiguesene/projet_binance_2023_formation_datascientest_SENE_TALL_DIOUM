import os

import numpy as np
import pandas as pd
from binance.client import Client
from joblib import load
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

# Parametres externalisés

#api_key = '7FipgVGJTbxWEyeyI5wNRyKuQwXXJcRIJBZvvQAxRY1aScVExHzdyQFMh3bLLPT5'
#api_secret = 'tnlNDg4WOt0xungysd7fAZAVKyBqqOzcgQW8MYebVo1piJzfeUC1mYkcDgJSm4T1'

# ELASTIC
# URL_ELASTIC = "http://54.195.84.110:9200"
URL_ELASTIC = "http://54.195.84.110:9200"
INDEX_ELASTIC = "cryptobot"


# HOST_MYSQL = 'localhost'
# BDNAME_MYSQL = 'cryptobot'
# USER_MYSQL = 'root'
# PASSWORD_MYSQL = 'Password'
# PORT_MYSQL = "3306"
# TABLENAME_MYSQL = "botmarche"


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


def predict(api_key, api_secret):
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
        X = preprocess_data(df)

        # load models from disk
        models = get_models(model_name='XGBoost', symbol=symbol)
        model_rf = models['model_xgb']

        prediction = model_rf.predict(X).tolist()
        data.append({"prediction": prediction, "symbol": symbol})