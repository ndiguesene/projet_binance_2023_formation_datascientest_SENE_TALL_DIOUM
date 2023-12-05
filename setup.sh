#docker-compose down

#docker container stop mysqldb
#docker container rm mysqldb
#
#docker container stop populate_db_mysql
#docker container rm populate_db_mysql

#docker image rm mysql
#docker image rm populate_into_mysql

cd ./populate_base
docker image build . -t populate_into_mysql:0.0.1

cd ./../api/
docker image build . -t api:0.0.1

cd ./../up

docker-compose up -d
