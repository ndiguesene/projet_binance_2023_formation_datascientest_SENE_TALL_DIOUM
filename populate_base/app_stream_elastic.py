# installation du package python-binance
# pip install python-binance

from binance.client import Client

# init
api_key = '7FipgVGJTbxWEyeyI5wNRyKuQwXXJcRIJBZvvQAxRY1aScVExHzdyQFMh3bLLPT5'
api_secret = 'tnlNDg4WOt0xungysd7fAZAVKyBqqOzcgQW8MYebVo1piJzfeUC1mYkcDgJSm4T1'

client = Client(api_key=api_key, api_secret=api_secret, testnet=True)

data = []
for marche in client.get_all_tickers():
    data.append(tuple(client.get_ticker(symbol=marche.get("symbol")).values()))

