import os
import warnings

import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from joblib import dump
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBClassifier

from constant import getBaseFromMysql

# HOST_MYSQL = 'localhost'
# BDNAME_MYSQL = 'cryptobot'
# USER_MYSQL = 'root'
# PASSWORD_MYSQL = 'Password'
# PORT_MYSQL = "3306"
# # PASSWORD_MYSQL = 'root'
# TABLENAME_MYSQL = "botmarche"
# api_key = '7FipgVGJTbxWEyeyI5wNRyKuQwXXJcRIJBZvvQAxRY1aScVExHzdyQFMh3bLLPT5'
# api_secret = 'tnlNDg4WOt0xungysd7fAZAVKyBqqOzcgQW8MYebVo1piJzfeUC1mYkcDgJSm4T1'

warnings.filterwarnings("ignore")


def custom_train_test_split(symbol_data, test_size=0.3):
    train_data = pd.DataFrame()
    test_data = pd.DataFrame()

    symbol_test_size = int(len(symbol_data) * test_size)

    symbol_X = symbol_data.drop('achat_vente', axis=1)
    symbol_y = symbol_data['achat_vente']

    symbol_data_train, symbol_data_test = train_test_split(
        symbol_data, test_size=symbol_test_size, shuffle=False
    )

    train_data = pd.concat([train_data, symbol_data_train])
    test_data = pd.concat([test_data, symbol_data_test])

    X_train, y_train = train_data.drop('achat_vente', axis=1), train_data['achat_vente']
    X_test, y_test = test_data.drop('achat_vente', axis=1), test_data['achat_vente']

    return X_train, X_test, y_train, y_test


def preprocess_data(X_train, X_test):
    # Encoding de la colonne 'symbol' avec LabelEncoder
    label_encoder = LabelEncoder()
    X_train['symbol'] = label_encoder.fit_transform(X_train['symbol'])
    X_test['symbol'] = label_encoder.transform(X_test['symbol'])

    # Normalisation des colonnes sélectionnées avec MinMaxScaler
    columns_to_normalize = ['open_price', 'close_price', 'volume', 'quote_asset_volume', 'number_of_trades',
                            'cumulative_volume', 'price_range', 'rolling_mean']
    min_max_scaler = MinMaxScaler()
    X_train[columns_to_normalize] = min_max_scaler.fit_transform(X_train[columns_to_normalize])
    X_test[columns_to_normalize] = min_max_scaler.transform(X_test[columns_to_normalize])

    return X_train, X_test


def smote_sampling(X_symbol, y_symbol):
    X_train_resampled = pd.DataFrame()
    y_train_resampled = pd.Series()

    unique_classes = np.unique(y_symbol)
    print(unique_classes)
    if len(unique_classes) > 1:
        smote = SMOTE(sampling_strategy='auto', random_state=42)
        try:
            X_resampled, y_resampled = smote.fit_resample(X_symbol, y_symbol)
            X_train_resampled = pd.concat([X_train_resampled, X_resampled])
            y_train_resampled = pd.concat([y_train_resampled, y_resampled])
        except ValueError as e:
            X_train_resampled = pd.concat([X_train_resampled, X_symbol])
            y_train_resampled = pd.concat([y_train_resampled, y_symbol])

    else:

        X_train_resampled = pd.concat([X_train_resampled, X_symbol])
        y_train_resampled = pd.concat([y_train_resampled, y_symbol])

    return X_train_resampled, y_train_resampled


def create_all_models():
    df = getBaseFromMysql()
    column_names = ['open_price', 'high_price', 'low_price', 'close_price', 'volume', 'quote_asset_volume',
                    'number_of_trades', 'open_time', 'close_time', 'symbol']
    df = df[column_names]

    symbols_to_filter = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "USDCUSDT", "BNBUSDT"]
    df = df[df['symbol'].isin(symbols_to_filter)]
    df.sort_values(by=['symbol', 'open_time'], inplace=True)

    # Création des indicateurs métiers
    df['cumulative_volume'] = df.groupby('symbol')['volume'].cumsum()
    df['price_range'] = df['close_price'] - df['open_price']
    df['rolling_mean'] = df.groupby('symbol')['close_price'].rolling(window=10).mean().reset_index(level=0, drop=True)
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
    df = df.drop(['open_time', 'close_time', 'high_price', 'low_price'], axis=1)

    df = pd.get_dummies(df, columns=['hour', 'day_of_week', 'month'])

    # Récupération des symboles uniques dans le dataset
    symbols = df['symbol'].unique()

    # Initialisation des résultats pour chaque modèle
    results = {}

    for symbol in symbols:
        try:
            symbol_data = df[df['symbol'] == symbol]

            # Custom train-test split
            X_train, X_test, y_train, y_test = custom_train_test_split(symbol_data, test_size=0.2)

            # Encodage et normalisation
            X_train, X_test = preprocess_data(X_train, X_test)

            # Suréchantillonnage
            X_train_resampled, y_train_resampled = smote_sampling(X_train, y_train)

            # Construction des modèles
            # models = {
            #     'XGBoost': XGBClassifier(random_state=42),
            # }
            models = {
                'Logistic_Regression': LogisticRegression(random_state=42),
                'Random_Forest': RandomForestClassifier(random_state=42),
                'Gradient_Boosting': GradientBoostingClassifier(learning_rate=0.01, n_estimators=50, random_state=42),
                'XGBoost': XGBClassifier(random_state=42),
                'SVM': svm.SVC()
            }

            for model_name, model in models.items():
                # Entraînement du modèle
                # print(X_train_resampled)
                # print(X_train_resampled.columns)
                model.fit(X_train_resampled, y_train_resampled)

                # Prédictions
                symbol_predictions = model.predict(X_test)

                # Calcul des métriques d'évaluation pour chaque modèle
                accuracy = accuracy_score(y_test, symbol_predictions)
                report = classification_report(y_test, symbol_predictions, output_dict=True)

                # Stockage des résultats pour chaque modèle
                if model_name not in results:
                    results[model_name] = {
                        'accuracy': [],
                        'precision': [],
                        'recall': [],
                        'f1-score': []
                    }

                results[model_name]['accuracy'].append(accuracy)
                results[model_name]['precision'].append(report['macro avg']['precision'])
                results[model_name]['recall'].append(report['macro avg']['recall'])
                results[model_name]['f1-score'].append(report['macro avg']['f1-score'])

                home_path = os.getcwd()
                print(home_path + "/opa_cypto_" + model_name + "_" + symbol + ".joblib")
                dump(model, home_path + "/opa_cypto_" + model_name + "_" + symbol + ".joblib")


        except ValueError as e:
            continue

    # Calcul de la moyenne globale pour chaque modèle
    # for model_name, metrics in results.items():
    #     print(f"\n{model_name} - Global Average Metrics")
    #     print(f"Accuracy: {np.mean(metrics['accuracy'])}")
    #     print(f"Precision: {np.mean(metrics['precision'])}")
    #     print(f"Recall: {np.mean(metrics['recall'])}")
    #     print(f"F1-score: {np.mean(metrics['f1-score'])}")

    return {"results": results.items()}
