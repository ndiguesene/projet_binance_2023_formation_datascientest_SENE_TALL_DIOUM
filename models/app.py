from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics


# Fonction pour obtenir des données historiques à partir de CSV
def get_data_historical(fileName, sep):
    import pandas as pd
    df = pd.read_csv(fileName, sep=sep)
    return df


# Fonction pour générer des caractéristiques simples pour la démonstration
def generate_features(df):
    df['price_variation'] = df['close_price'].pct_change()
    df['target'] = (df['price_variation'] >= 0).astype(int)
    return df.dropna()

symbol = "ETHBTC"
# Charger les données historiques pour le symbole BTC/USDT
data = get_data_historical("./../botmarche.csv", sep=",")
data = data[data['symbol'] == symbol]
dataFeatures = generate_features(data)
print(dataFeatures)

# Diviser les données en ensembles d'entraînement et de test
train_data, test_data = train_test_split(dataFeatures, test_size=0.2, shuffle=False)

# Séparer les caractéristiques et les cibles
features = ['open_price', 'high_price', 'low_price', 'close_price', 'volume']
X_train, y_train = train_data[features], train_data['target']
X_test, y_test = test_data[features], test_data['target']

# Créer et entraîner le modèle (Régression Logistique pour cet exemple)
model = LogisticRegression()
model.fit(X_train, y_train)

# Faire des prédictions sur l'ensemble de test
predictions = model.predict(X_test)

# Évaluer la performance du modèle
accuracy = metrics.accuracy_score(y_test, predictions)
print(f'Accuracy: {accuracy}')

# Exemple de stratégie de trading basée sur les prédictions
for i in range(len(predictions)):
    if predictions[i] == 1:
        print(f"Buy {symbol} at {test_data['close_price'].iloc[i]}")
    else:
        print(f"Sell {symbol} at {test_data['close_price'].iloc[i]}")
