# Projet Final: OPA Crypto

## Objectifs

Ce repository contient les rendus du projet final. L'objectif étant de créer une API qui requête des données depuis ue
base de données préalablement peuplée et une autre API pour le train de notre model et autres.
Les données utilisées concernent les données Binance, API de collecte de données. Le schéma des données et l'API est le
suivant:

## Description de chaque colonne et API consommé depuis BINANCE

### Description

1. id
2. open_price
3. high_price
4. low_price
5. close_price
6. volume
7. quote_asset_volume
8. number_of_trades
9. kline_open_time_parsed
10. kline_close_time_parsed
11. symbol

### API Binance

## Choix des base de données

2 base de données sont utilisées dans le cadre ce projet, MySQL et ElasticSearch

- La base MySQL nous permettra de la peupler à partir des données historique de Binance a des fins d'entrainement de
  notre model machine learning(Des APIs seront créées pour afficher les données se trouvant dans MySQL)
- La base Elastic, nous permettra de stocker les données fraichement récupérer depuis l'API, avec l'outils Kibana on
  pourra créer des Dashboard.(C'est l'un des meilleurs outils combiné avec Elastic)

## Requêtage de base de données

Nous avons utilisé `FastAPI`, la librairie python-binance ainsi que la librairie MySQL connector.
FastAPI nous permet de créer les routes d'api à utiliser par les utilisateurs pour interagir avec la base de données.
le module `mysql-connector` a été utilisé pour gérer le peuplement de la base de données.

## Fichiers

1. Le fichier `setup.sh` contient les commandes de création des images et conteneurs de peuplement de la base de
   données, de l'image et du conteneur de création de la base de données ainsi que l'API de requêtage de la base de
   données et celui du model dont une API a été créée pour l'entrainement du model
2. Le dossier `api` contient le Dockerfile pour créer l'image docker contenant la logique de l'API (récupérer les
   données depuis MySQL), un fichier api.py contenant la logique de l'API ainsi qu'un fichier requirements informant sur
   les prérequis d'exécution
3. Le dossier `models` contient le Dockerfile pour créer l'image docker contenant la logique du model, un fichier api.py
   contenant la logique de l'API ainsi qu'un fichier requirements informant sur les prérequis d'exécution
4. Le dossier `populate_base/mysql` contient le dockerfile de création de lancement contenant la logique de peuplement
   de la bdd MySQL, un fichier app.py contenant la logique
5. Le dossier `up` contient le fichier compose permettant de lancer tous les conteneurs docker

## Utilisation de l'application

Lancer les différents images et conteneurs et puis l'exécuter:
> > chmod +x setup.sh    
> > sh setup.sh  
