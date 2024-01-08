import datetime

import pandas as pd
# Importation de la dépendance python-binance apres installation avec pip install pythnn-binance
from binance import Client

# Tout d’abords nous avons créé notre API_KEY et API_SECRET depuis la plateforme afin de l’utiliser dans notre programme de récupération de données
api_key = '7FipgVGJTbxWEyeyI5wNRyKuQwXXJcRIJBZvvQAxRY1aScVExHzdyQFMh3bLLPT5'
api_secret = 'tnlNDg4WOt0xungysd7fAZAVKyBqqOzcgQW8MYebVo1piJzfeUC1mYkcDgJSm4T1'
end_date = datetime.datetime.now()
# On prends une historique de données de 60 jours glissants
start_date = end_date - datetime.timedelta(days=1)  # 30 days ago

# Convert dates to milliseconds (required by Binance API)
start_timestamp = int(start_date.timestamp() * 1000)
end_timestamp = int(end_date.timestamp() * 1000)

# Instanciation d’objet Client
client = Client(api_key=api_key, api_secret=api_secret, testnet=True)
# Requeter les données historique d'un jour pour le symbol(marche) BTCUSDT
historical_prices = client.get_historical_klines('BTCUSDT', Client.KLINE_INTERVAL_1HOUR, start_timestamp,
                                                 end_timestamp)
# Créer un DataFrame à partir des données historiques
columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume',
           'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']
df = pd.DataFrame(historical_prices, columns=columns)
print(df)
# Convertir le DataFrame en format JSON avec les colonnes
json_data = df.to_json(orient='records')

# Affichage du résultat (facultatif)
print(json_data)

# Enregistrer le JSON dans un fichier
with open('historical_data.json', 'w') as file:
    file.write(json_data)
