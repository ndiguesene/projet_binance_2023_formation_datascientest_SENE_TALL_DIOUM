import pandas as pd
from joblib import dump
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def get_data_historical(fileName, sep):
    df = pd.read_csv(fileName, sep=sep)
    return df


def get_all_symbols(client):
    data = []
    for marche in client.get_all_tickers():
        data.append(marche.get("symbol"))
    return data


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

    dump(model, "./opa_cypto_model_rl.joblib")


def create_random_forest_model(link="../botmarche_ok.csv"):
    data = get_data_historical(link, sep=",")
    # Identification de la variable de temps
    data['timestamp'] = data['kline_close_time_parsed']
    # La moyenne mobile sur une fenêtre de 10 périodes pour la colonne 'close_price'
    # (Indicateur Technique dans l'analyse financiere (moyennemobile)
    data['moyennemobile10'] = data['close_price'].rolling(window=10).mean()
    data.loc[data['close_price'] == data['moyennemobile10'], 'prediction'] = 0  # Pas de choix de prédition
    data.loc[
        data['close_price'] < data['moyennemobile10'], 'prediction'] = -1  # C'est si le prix dimunera pour la vente
    data.loc[
        data['close_price'] > data['moyennemobile10'], 'prediction'] = 1  # C'est si le prix augmentera pour l'achat

    df = data.dropna()

    # Séparer les données en ensembles d'entraînement et de test
    # L'intégration de la variable 'number_of_trades' n'a pas une forte impacte sur la variable à expliquer y
    X = df[['open_price', 'high_price', 'low_price', 'close_price', 'volume', 'moyennemobile10']]
    y = df['prediction']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Créer un modèle de classification (par exemple, RandomForest)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Prédictions sur l'ensemble de test
    predictions = model.predict(X_test)

    # Calcul de la précision du modèle
    accuracy = accuracy_score(y_test, predictions)
    print(f'Précision du modèle : {accuracy}')

    # Faire des prédictions sur l'ensemble de test
    # predictions = model.predict(X_test)
    dump(model, "./opa_cypto_model_rf.joblib")
    return {"score": str(accuracy)}


if __name__ == "__main__":
    create_random_forest_model(link="../botmarche_ok.csv")
    # create_logistic_regression_model(data)
