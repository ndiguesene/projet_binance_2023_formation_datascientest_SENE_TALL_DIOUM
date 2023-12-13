from binance.client import Client
from confluent_kafka import Producer
from constant import api_key, api_secret

# Configuration de l'API Binance
api_key = 'VOTRE_API_KEY'
api_secret = 'VOTRE_API_SECRET'

# Configuration Kafka
bootstrap_servers = 'http://localhost:9092'  # Remplacez-le par votre liste de brokers Kafka
topic_name = 'cyptobot'  # Nom du topic Kafka

# Initialisation du client Binance
client = Client(api_key, api_secret)

# Configuration du producer Kafka
producer = Producer({'bootstrap.servers': bootstrap_servers})

# Fonction pour envoyer les données à Kafka
def send_to_kafka(symbol, data):
    try:
        producer.produce(topic_name, key=symbol, value=data)
        producer.flush()
        print(f"Message envoyé à Kafka pour {symbol}: {data}")
    except Exception as e:
        print(f"Erreur lors de l'envoi à Kafka: {str(e)}")

# Liste des symboles Binance à surveiller
symbols = ["BTCUSDT", "ETHUSDT"]  # Exemple de symboles

# Récupération des données pour chaque symbole et envoi à Kafka
for symbol in symbols:
    klines = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE)
    for kline in klines:
        send_to_kafka(symbol, str(kline))

# Fermer le producer Kafka
producer.close()
