docker-compose down

docker container stop populate_db
docker container rm populate_db

docker container stop query_db
docker container rm query_db

docker image rm projet3-de/api:0.0.1
docker image rm projet3-de/populate:0.0.1

cd populate/
docker image build . -t projet3-de/populate:0.0.1

cd ..

cd api/
docker image build . -t projet3-de/api:0.0.1

cd ..

cd up/

docker-compose up -d
