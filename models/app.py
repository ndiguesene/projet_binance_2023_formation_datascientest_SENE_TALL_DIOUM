import mysql.connector
import pandas as pd
from joblib import dump
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from constant import HOST_MYSQL, PORT_MYSQL, BDNAME_MYSQL, USER_MYSQL, PASSWORD_MYSQL, TABLENAME_MYSQL


def get_data_historical(fileName, sep):
    df = pd.read_csv(fileName, sep=sep)
    return df


def get_data_historical(fileName, sep):
    df = pd.read_csv(fileName, sep=sep)
    return df


def get_all_symbols(client):
    data = []
    for marche in client.get_all_tickers():
        data.append(marche.get("symbol"))
    return data


mydb = mysql.connector.connect(host=HOST_MYSQL,
                               port=PORT_MYSQL,
                               database=BDNAME_MYSQL,
                               user=USER_MYSQL,
                               password=PASSWORD_MYSQL)


def getBaseFromMysql():
    # cursor = mydb.cursor()
    # cursor.execute("SELECT * FROM {}.{}".format(BDNAME_MYSQL, TABLENAME_MYSQL))
    # result = cursor.fetchall()
    data_frame = pd.read_sql("SELECT * FROM {}.{}".format(BDNAME_MYSQL, TABLENAME_MYSQL), mydb)

    # columns = [i[0] for i in cursor.description]
    # print(columns)
    # data_frame = pd.DataFrame(result, columns=columns)
    # print(data_frame)
    mydb.close()
    return data_frame


def create_logistic_regression_model(link="../botmarche_ok.csv"):
    data = get_data_historical(link, sep=",")
    # Identification de la variable de temps
    data['timestamp'] = data['kline_close_time_parsed']
    data['moyennemobile10'] = data['close_price'].rolling(window=10).mean()
    data.loc[data['close_price'] == data['moyennemobile10'], 'prediction'] = 0
    data.loc[data['close_price'] < data['moyennemobile10'], 'prediction'] = -1
    data.loc[data['close_price'] > data['moyennemobile10'], 'prediction'] = 1
    # Suppression des valeurs NULL
    df = data.dropna()

    # Séparer les données en ensembles d'entraînement et de test
    X = df[['open_price', 'high_price', 'low_price', 'close_price', 'volume', 'moyennemobile10']]
    y = df['prediction']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Créer un modèle de classification (par exemple, RandomForest)
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Prédictions sur l'ensemble de test
    predictions = model.predict(X_test)

    # Calcul de la précision du modèle
    accuracy = accuracy_score(y_test, predictions)
    print(f'Précision du modèle : {accuracy}')
    print("RMSE:", predictions.summary.rootMeanSquaredError)
    rmse = predictions.summary.rootMeanSquaredError
    print("R2:  ", predictions.summary.r2)
    r2 = predictions.summary.r2

    dump(model, "./opa_cypto_model_rl.joblib")
    return {"score": str(accuracy), "RMSE": str(rmse), "r2": str(r2)}


def create_random_forest_model(link="../botmarche_ok.csv"):
    data = get_data_historical(link, sep=",")
    # data = data[(data["symbol"] == "ETHBTC")]
    # Identification de la variable de temps
    data['timestamp'] = pd.to_datetime(data['kline_close_time_parsed']).astype(int) / 10 ** 9

    # La moyenne mobile sur une fenêtre de 10 périodes pour la colonne 'close_price'
    # (Indicateur Technique dans l'analyse financiere (moyennemobile)
    data['moyennemobile10'] = data['close_price'].rolling(window=10).mean()
    data.loc[data['close_price'] == data['moyennemobile10'], 'prediction'] = 0  # Pas de choix de prédition
    data.loc[
        data['close_price'] < data['moyennemobile10'], 'prediction'] = -1  # C'est si le prix dimunera pour la vente
    data.loc[
        data['close_price'] > data['moyennemobile10'], 'prediction'] = 1  # C'est si le prix augmentera pour l'achat
    data = data.dropna()

    # Séparer les données en features et target
    X = data[['open_price', 'high_price', 'low_price', 'volume', 'moyennemobile10', 'timestamp']]
    y = data['prediction']
    symbol = data['symbol']

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)
    symbol = label_encoder.fit_transform(symbol)

    # Diviser les données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test, symbol_train, symbol_test = train_test_split(X, y, symbol, test_size=0.2,
                                                                                   random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=33)

    # Entraîner le modèle
    model.fit(X_train, y_train)

    # Obtenir les prédictions pour les données de test
    predictions = model.predict(X_test)

    # Associer les prédictions aux symboles
    predicted_markets = label_encoder.inverse_transform(predictions)  # Inverse de l'encodage des symboles

    # Afficher les prédictions pour chaque marché
    # Évaluation du modèle
    accuracy = model.score(X_test, y_test)
    print(predictions)
    print("Accuracy:", accuracy_score(y_test, predictions))
    # print(classification_report(y_test, predictions))
    print(predicted_markets)

    # -1 => 0  Pas de choix de prédition
    #  0 => 1  le prix dimunera pour la vente
    #  1 => 2  le prix augmentera pour l'achat
    # print(predicted_markets)
    # for i, market in enumerate(predicted_markets):
    #    print(f"N {i + 1}: Prédiction : {predictions[i]} - du Symbol: {market}")

    print(classification_report(y_test, predictions))
    dump(model, "./opa_cypto_model_rf.joblib")
    return {"score": str(accuracy)}


def create_random_forest_model():
    data = getBaseFromMysql()
    print(data.columns)
    data['timestamp'] = pd.to_datetime(data['kline_close_time_parsed']).astype(int) / 10 ** 9

    # La moyenne mobile sur une fenêtre de 10 périodes pour la colonne 'close_price'
    # (Indicateur Technique dans l'analyse financiere (moyennemobile)
    data['moyennemobile10'] = data['close_price'].rolling(window=10).mean()
    data.loc[data['close_price'] == data['moyennemobile10'], 'prediction'] = 0  # Pas de choix de prédition
    data.loc[
        data['close_price'] < data['moyennemobile10'], 'prediction'] = -1  # C'est si le prix dimunera pour la vente
    data.loc[
        data['close_price'] > data['moyennemobile10'], 'prediction'] = 1  # C'est si le prix augmentera pour l'achat
    data = data.dropna()

    # Séparer les données en features et target
    X = data[['open_price', 'high_price', 'low_price', 'volume', 'moyennemobile10', 'timestamp']]
    y = data['prediction']
    symbol = data['symbol']

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)
    symbol = label_encoder.fit_transform(symbol)

    # Diviser les données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test, symbol_train, symbol_test = train_test_split(X, y, symbol, test_size=0.2,
                                                                                   random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=33)

    # Entraîner le modèle
    model.fit(X_train, y_train)

    # Obtenir les prédictions pour les données de test
    # predictions = model.predict(X_test)

    # Associer les prédictions aux symboles
    # predicted_markets = label_encoder.inverse_transform(predictions)  # Inverse de l'encodage des symboles

    # Afficher les prédictions pour chaque marché
    # Évaluation du modèle
    accuracy = model.score(X_test, y_test)
    # print(predictions)
    # print("Accuracy:", accuracy_score(y_test, predictions))
    # print(classification_report(y_test, predictions))
    # print(predicted_markets)

    # -1 => 0  Pas de choix de prédition
    #  0 => 1  le prix dimunera pour la vente
    #  1 => 2  le prix augmentera pour l'achat
    # print(predicted_markets)
    # for i, market in enumerate(predicted_markets):
    #    print(f"N {i + 1}: Prédiction : {predictions[i]} - du Symbol: {market}")

    # print(classification_report(y_test, predictions))
    dump(model, "./opa_cypto_model_rf.joblib")
    return {"score": str(accuracy)}

# if __name__ == "__main__":
#    create_random_forest_model()
