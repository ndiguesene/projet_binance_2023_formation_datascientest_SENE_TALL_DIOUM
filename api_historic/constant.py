import mysql.connector
import pandas as pd

# Parametres externalisés

# api_key = '7FipgVGJTbxWEyeyI5wNRyKuQwXXJcRIJBZvvQAxRY1aScVExHzdyQFMh3bLLPT5'
# api_secret = 'tnlNDg4WOt0xungysd7fAZAVKyBqqOzcgQW8MYebVo1piJzfeUC1mYkcDgJSm4T1'

# ELASTIC
# URL_ELASTIC = "http://54.195.84.110:9200"
URL_ELASTIC = "http://54.195.84.110:9200"
INDEX_ELASTIC = "cryptobot"

# MYSQL
HOST_MYSQL = "db"
PORT_MYSQL = "3306"
BDNAME_MYSQL = "cryptobot"
TABLENAME_MYSQL = "botmarche"
USER_MYSQL = "root"
PASSWORD_MYSQL = "root"


# HOST_MYSQL = 'localhost'
# BDNAME_MYSQL = 'cryptobot'
# USER_MYSQL = 'root'
# PASSWORD_MYSQL = 'Password'
# PORT_MYSQL = "3306"
# # PASSWORD_MYSQL = 'root'
# TABLENAME_MYSQL = "botmarche"
# api_key = '7FipgVGJTbxWEyeyI5wNRyKuQwXXJcRIJBZvvQAxRY1aScVExHzdyQFMh3bLLPT5'
# api_secret = 'tnlNDg4WOt0xungysd7fAZAVKyBqqOzcgQW8MYebVo1piJzfeUC1mYkcDgJSm4T1'

def getConnexionMysql():
    max_attempts = 30
    attempts = 0
    connected = False
    # Cette partie permet d'etre sur que le mysql est ready, parce que
    # Docker ne garantit pas nécessairement l'ordre de démarrage des services, ce qui peut entraîner le démarrage de votre service Python (app) avant que le service de la base de données MySQL (db)
    # ne soit prêt
    connection_return = None
    import time

    while not connected and attempts < max_attempts:
        try:
            connection_return = mysql.connector.connect(host=HOST_MYSQL,
                                                        port=PORT_MYSQL,
                                                        database=BDNAME_MYSQL,
                                                        user=USER_MYSQL,
                                                        password=PASSWORD_MYSQL)
            connected = True
            print("MySQL is ready!")
        except mysql.connector.Error as err:
            print(f"Attempt {attempts + 1}: MySQL is not ready yet - Error: {err}")
            attempts += 1
            time.sleep(10)
    return connection_return


def getBaseFromMysql():
    connection = getConnexionMysql()
    mycursor = connection.cursor()
    mycursor.execute("SELECT * FROM {}.{}".format(BDNAME_MYSQL, TABLENAME_MYSQL))
    myresult = mycursor.fetchall()
    data_frame = pd.DataFrame(myresult, columns=[i[0] for i in mycursor.description])
    connection.close()
    return data_frame
