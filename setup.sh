docker-compose down

docker container stop populate_mysql_data_binance
docker container rm populate_mysql_data_binance


cd populate/
docker image build . -t projet3-de/populate:0.0.1

cd ..

cd api/
docker image build . -t projet3-de/api:0.0.1

cd ..

cd up/

docker-compose up -d
