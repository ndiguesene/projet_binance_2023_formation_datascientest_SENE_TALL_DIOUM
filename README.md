# Projet3: Base de données

### Objectifs
Ce repository contient les rendus du projet 3. L'objectif étant de créer une API qui requête des données depuis ue base de données préalablement peuplée.
Les données utilisées concernent une publication de produits de Amazon. Le schéma des données est le suivant: 
1. uniq_id
2. product_name,
3. manufacturer
4. price
5. number_available_in_stock
6. number_of_reviews
7. number_of_answered_questions
8. average_review_rating
9. amazon_category_and_sub_category
10. customers_who_bought_this_item_also_bought
11. description
12. product_information
13. product_description
14. items_customers_buy_after_viewing_this_item
15. customer_questions_and_answers
16. customer_reviews
17. sellers  


La descrition des colonnes est disponibles sur le site data.world (https://data.world/promptcloud/fashion-products-on-amazon-com). Nous avons travaillé avec MongoDB pour sauvegarder les données.

### Choix de la base de données
Les données que nous avons considérées sont des données descriptives de produits vendus sur Amazon. Tous les produits sont censés posséder les mêmes éléments. Vue la nature de l'activité qui génère ces données, certains lignes de données peuvent ne pas être renseignées telles les commentaires utilisateurs, les questions des utilisateurs ainsi que les notes données aux produits par les utilisateurs. Les produits peuvent donc ne pas contenir les mêmes élements dans la base. Nous avons donc choisi de passer sur une SGBD NoSQL.

### Requêtage de base de données
Nous avons utilisé FastAPI, la librairie PyMongo ainsi que la librairie Motor de MongoDB.
FastAPI nous permet de créer les routes d'api à utiliser par les utilisateurs pour interagir avec la base de données.
PyMongo a été utilisé pour gérer le peuplement de la base de données.
Nous avons exploré l'utilisation de Motor (https://motor.readthedocs.io/en/stable/) pour gérer les requêtes avec la base de données. Cette librairie est cencée gérer les requêtes avec la base de données d'une manière non bloquante.

### Fichiers
1. Le fichier `setup.sh` contient les commandes de création des images et conteneurs de peuplement de la base de données, de l'image et du conteneur de création de la base de données ainsi que l'API de requêtage de la base de données
2. Le dossier `api` contient le Dockerfile pour créer l'image docker contenant la logique de l'API, un fichier api.py contenant la logique de l'API ainsi qu'un fichier requirements informant sur les prérequis d'exécution
3. Le dossier `populate` contient le dockerfile de création de lancement contenant la logique de peuplement de la bdd, un fichier app.py cotent la logique et un fichier requirements
4. Le dossier `up` contient le fichier compose permettant de lancer tous les conteneurs docker

### Utilisation de l'application
Lancer les différents images et conteneurs:
>> chmod +x setup.sh    
>> sh setup.sh  

Vous pouvez tester et consulter la documentation de l'API sur http://0.0.0.0:8000/docs après lancement.  
Il vous faut au préalable créer un tunel ssh entre l'API et le port 8000 de votre machine.  Un exemple ci-après.

>> ssh -i "data_enginering_machine.pem" ubuntu@3.251.80.227 -fNL 8000:192.168.49.2:80

Et donc par la suite l'api s'ouvre sur le navigateur sur l'adresse  localhost:8000/docs.  
`Nota`: L'utilisation de l'API se fait par corps de requête

#### Routes

###### Lire `n`documents de la collection
>> curl -X 'GET' \
  'http://localhost:8000/read/document?n=2' \
  -H 'accept: application/json'

Réponse de l'api :

{
  "data": [
    [
      {
        "id": "6341f586bae80733eb130a20",
        "product_name": "Hornby 2014 Catalogue",
        "manufacturer": "Hornby",
        "price": "£3.42",
        "number_available_in_stock": "5 new",
        "number_of_reviews": "15",
        "number_of_answered_questions": 1,
        "average_review_rating": "4.9 out of 5 stars",
        "amazon_category_and_sub_category": "Hobbies > Model Trains & Railway Sets > Rail Vehicles > Trains",
        ...
      },
      {
        "id": "6341f586bae80733eb130a21",
        "product_name": "FunkyBuys® Large Christmas Holiday Express Festive Train Set (SI-TY1017) Toy Light / Sounds / Battery Operated & Smoke",
        "manufacturer": "FunkyBuys",
        "price": "£16.99",
        "number_available_in_stock": "N/A",
        "number_of_reviews": "2",
        "number_of_answered_questions": 1,
        "average_review_rating": "4.5 out of 5 stars",
        "amazon_category_and_sub_category": "Hobbies > Model Trains & Railway Sets > Rail Vehicles > Trains",
        "customers_who_bought_this_item_also_bought": "http://www.amazon.co.uk/Christmas-Holiday-Express-Festive-Train-Set-Toy/dp/B009R8S8AA | http://www.amazon.co.uk/Goldlok-Holiday-Express-Operated-Multi-Colour/dp/B009R8PAO2 | http://www.amazon.co.uk/FunkyBuys%C2%AE-Christmas-SI-TY1017-Ornaments-Operated/dp/B01437QMHA | http://www.amazon.co.uk/Holiday-Express-Christmas-Ornament-Decoration | http://www.amazon.co.uk/Seasonal-Vision-Christmas-Tree-Train/dp/B0044ZC1W2 | http://www.amazon.co.uk/Coca-Cola-Santa-Express-Train-Set/dp/B004BYSNU0",
        "description": "Size Name:Large FunkyBuys® Large Christmas Holiday Express Festive Train Set (SI-TY1017) Toy Light / Sounds / Battery Operated & Smoke",
        "product_information": "Technical Details Manufacturer recommended age:3 years and up Item model numberSI-TY1017-B    Additional Information ASINB01434AIRS Best Sellers Rank 169,625 in Toys & Games (See top 100) #261 in Toys & Games > Model Trains & Railway Sets > Rail Vehicles > Trains Delivery Destinations:Visit the Delivery Destinations Help page to see where this item can be delivered. Date First Available18 Aug. 2015   ",
        "product_description": "Size Name:Large FunkyBuys® Large Christmas Holiday Express Festive Train Set (SI-TY1017) Toy Light / Sounds / Battery Operated & Smoke",
        "items_customers_buy_after_viewing_this_item": "http://www.amazon.co.uk/Christmas-Holiday-Express-Festive-Train-Set-Toy/dp/B009R8S8AA | http://www.amazon.co.uk/Goldlok-Holiday-Express-Operated-Multi-Colour/dp/B009R8PAO2 | http://www.amazon.co.uk/FunkyBuys%C2%AE-Christmas-SI-TY1017-Ornaments-Operated/dp/B01437QMHA | http://www.amazon.co.uk/Holiday-Express-Christmas-Ornament-Decoration",
        "customer_questions_and_answers": "can you turn off sounds // hi no you cant turn sound off",
        "customer_reviews": "Four Stars // 4.0 // 18 Dec. 2015 // By\n    \n    kenneth bell\n  \n on 18 Dec. 2015 // Very happy with the communication with funkybuys | Five Stars // 5.0 // 14 Jan. 2016 // By\n    \n    moosixty\n  \n on 14 Jan. 2016 // Great buy.",
        "sellers": "{\"seller\"=>{\"Seller_name_1\"=>\"UHD WHOLESALE\", \"Seller_price_1\"=>\"£16.99\"}}"
      }
    ]
  ],
  "code": 200,
  "message": "Products retrieved successfully"
}

###### Ajouter un produit dans la collection 

>> curl -X 'POST' \
  'http://localhost:8000/add/document' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "uniq_id": "anewlyaddedproduct123456",
  "product_name": "Fashionista'\''s shoes",
  "manufacturer": "Fashionista",
  "price": "£13.4",
  "number_available_in_stock": "20 new",
  "number_of_reviews": 10,
  "number_of_answered_questions": 0,
  "average_review_rating": "3.2 out of 5 stars",
  "amazon_category_and_sub_category": "Women > Fashion > Shoes > High Heel",
  "customers_who_bought_this_item_also_bought": "N/A",
  "description": "A pair of high heels red shoes",
  "product_information": "N/A",
  "product_description": "N/A",
  "items_customers_buy_after_viewing_this_item": "N/A",
  "customer_questions_and_answers": "N/A",
  "customer_reviews": "N/A",
  "sellers": "N/A"
}'

Réponse de l'api : 

{
  "data": [
    {
      "id": "6341f74792acf7742fa3cfb3",
      "product_name": "Fashionista's shoes",
      "manufacturer": "Fashionista",
      "price": "£13.4",
      "number_available_in_stock": "20 new",
      "number_of_reviews": 10,
      "number_of_answered_questions": 0,
      "average_review_rating": "3.2 out of 5 stars",
      "amazon_category_and_sub_category": "Women > Fashion > Shoes > High Heel",
      "customers_who_bought_this_item_also_bought": "N/A",
      "description": "A pair of high heels red shoes",
      "product_information": "N/A",
      "product_description": "N/A",
      "items_customers_buy_after_viewing_this_item": "N/A",
      "customer_questions_and_answers": "N/A",
      "customer_reviews": "N/A",
      "sellers": "N/A"
    }
  ],
  "code": 200,
  "message": "Product add success."
}


