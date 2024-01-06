# Projet Final: OPA Crypto

Le monde financier évolue à une vitesse vertigineuse, 
porté par l'émergence des technologies avancées.
Dans ce contexte en perpétuel changement, l'automatisation des processus
de trading devient un enjeu majeur pour les acteurs du marché. 
C'est dans cette optique que nous avons choisi ce projet, 
qui nous permettra d'acquérir de nouvelles connaissances du marché financier 
tout en mettant en pratique notre formation.
L'objectif principal est la création d'un dashbord (bot de trading) novateur,
reposant sur un modèle de Machine Learning. Plus spécifiquement, 
ce bot sera conçu pour investir ou vendre dans les marchés crypto,
un secteur dynamique en constante évolution.

Le déploiement de stratégies automatisées dans le domaine 
des crypto-monnaies offre des perspectives fascinantes, 
mais également des défis complexes. En combinant les principes 
du Machine Learning avec l'analyse approfondie des marchés crypto, 
notre projet vise à élaborer un dashbord intelligent et adaptable, 
capable de prendre des décisions de trading dans des conditions 
de marché changeantes.

Au fil de ce repository, nous explorerons les fondements théoriques
de notre approche, les méthodologies employées pour développer
le modèle de Machine Learning, ainsi que les défis spécifiques liés 
à la conception d'un dashbord de trading performant
dans l'univers des crypto-monnaies. 

Ce projet est faites en 4 étapes partant sur la collecte et 
l'explotation des données depuis un API BINANCE, ensuite l'architecture 
des données avec MYSQL, puis la consommation de la donnée avec un modele 
machine learning et stockage dans Elasticsearch, et enfin une mise en production avec 
test du modèle et Dashboard Kibana.

En suivant ces étapes séquentielles, notre projet vise à mettre en œuvre
un bot de trading sophistiqué basé sur le Machine Learning,
capable de tirer parti des données provenant de l'API Binance
pour prendre des décisions éclairées sur les marchés crypto,
tout en stockant et en visualisant efficacement les résultats à l'aide
d'Elasticsearch et Kibana.

###### 1- Collecte des Données depuis l'API Binance

La première phase de notre projet consiste à recueillir de manière systématique
des données pertinentes à partir de l'API Binance. 
Cette étape essentielle nous permettra d'obtenir un flux continu
de données sur les marchés crypto, couvrant des aspects 
tels que les prix des actifs, les volumes d'échange et
d'autres indicateurs clés. La qualité et l'intégrité 
des données collectées joueront un rôle crucial 
dans la performance ultérieure de notre modèle de Machine Learning.

#### a - processus d'utilisation de l'API BINANCE
L'API BINANCE est une interface de programmation informatique
qui permet aux developpeurs d'interagir avec la plateforme d'échange 
de crypto-monnaies Binance. 
Le processus de récupération de données se fait en 5 étapes :
1- Création d'un Compte sur Binance
2- Activation de l'API sur Binance
3- Génération de la Clé API et du Secret API
4- Utilisation de la Clé API dans notre Projet
5- Récupération des données.

Après récupérutions des données, en dessous les définitions des variables 
de notre base de données. Cela est importante pour comprendre
le marché financier et pouvoir construire un modèle ML performant.

### Description

1. id : id unique associé à la transaction
2. open_price : Prix d'ouverture d'une période donnée, le prix auquel l'actif a commencé la période
3. high_price : Prix le plus élevé atteint au cours de la période donnée
4. low_price : Prix le plus bas atteint au cours de la période considérée
5. close_price : Prix de clôture d'une période donnée. C'est le prix auquel l'actif a été échangé avant la fin de la période
6. volume : Le volume d'échange, représentant la quantité totale d'un actif qui a été échangée au cours de la période donnée
7. quote_asset_volume : Le volume total en termes de devise de cotation (la deuxième devise dans une paire de trading) échangé au cours de la période donnée.
8. number_of_trades : Le nombre total de transactions exécutées au cours de la période.
9. kline_open_time_parsed : ate et heure d'ouverture de la transaction, exprimées dans un format lisible.
10. kline_close_time_parsed : Date et heure de clôture de la transaction, exprimées dans un format lisible.
11. symbol : La paire de trading associée aux données, indiquant quelles cryptomonnaies sont échangées l'une contre l'autre. Par exemple, dans la paire BTC/USDT, BTC est la devise de base et USDT est la devise de cotation




##### 2-  Architecture des Données avec MySQL

Une fois les données collectées, la deuxième étape consistera à concevoir 
une architecture robuste pour les stocker. Nous utiliserons MySQL,
un système de gestion de base de données relationnelle,
pour organiser et stocker les informations de manière structurée.
Cette architecture de données bien définie facilitera l'accès, 
la gestion et la manipulation des données, fournissant ainsi 
une base solide pour le développement ultérieur du modèle de Machine Learning.

## Requêtage de base de données

Nous avons utilisé `FastAPI`, la librairie `python-binance` ainsi que la librairie 
`MySQL connector` et d'autres dépendances nécessaires.
FastAPI nous permet de créer les routes d'api à utiliser par les utilisateurs 
pour interagir avec la base de données.le module `mysql-connector` a été utilisé
pour gérer le peuplement de la base de données.

## Fichiers

1. Le fichier `setup.sh` contient les commandes de création des images et conteneurs de peuplement de la base de
   données, de l'image et du conteneur de création de la base de données ainsi que l'API de requêtage de la base de
   données et celui du model dont une API a été créée pour l'entrainement du model
2. Le dossier `api_historic` contient le Dockerfile pour créer l'image docker contenant la logique de l'API (récupérer l'historique des données stocker dans MySQL)
3. Le dossier `models` contient le Dockerfile pour créer l'image docker contenant la logique de l'API pour entrainer notre model
4. Le dossier `elasticsearch` contient le Dockerfile pour créer l'image docker contenant la logique d'ingestion du résultat du model
5. Le dossier `populate_base/mysql` contient le dockerfile de création de lancement contenant la logique de peuplement
   de la bdd MySQL, un fichier app.py contenant la logique
6. Le dossier `up` contient le fichier docker compose permettant de lancer tous les conteneurs docker

## Utilisation de l'application

Lancer les différentes images et conteneurs et puis l'exécuter:
> > chmod +x setup.sh    
> > sh setup.sh  


###### 3- Consommation de la Donnée avec le Modèle de Machine Learning et Stockage dans Elasticsearch

Avec les données correctement archivées dans MySQL, nous utiliserons Elasticsearch 
pour stocker les résultats provenant du modèle de Machine Learning. Ce moteur de recherche et
d'analyse distribué permettra un stockage efficace et une recherche rapide 
des données générées par le modèle. Notre modèle de Machine Learning consommera 
les données stockées dans MySQL, analysera intelligemment ces informations,
et les résultats pertinents seront stockés dans Elasticsearch.

##### 4- Mise en Production avec Test du Modèle et Dashboard Kibana

La dernière étape du projet impliquera la mise en production du modèle de Machine Learning. 
Nous testerons rigoureusement le modèle dans un environnement simulé 
et réel pour évaluer sa performance et son adaptabilité aux conditions de marché 
variables. De plus, nous créerons un tableau de bord interactif à l'aide de Kibana, 
offrant une visualisation claire des résultats du modèle et 
des statistiques pertinentes. Ce tableau de bord facilitera
la surveillance continue et la prise de décision informée, 
tout en fournissant des insights précieux aux intervenants du projet.




