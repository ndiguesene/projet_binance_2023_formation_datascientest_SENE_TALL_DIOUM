cd ./populate_base/mysql
docker image build --no-cache . -t projet_final/populate_into_mysql:0.0.1

cd ./../../elasticsearch
docker image build --no-cache . -t projet_final/populate_into_elasticsearch:0.0.1

cd ./../models/
docker image build --no-cache . -t projet_final/model:0.0.1

cd ./../api_historic/
docker image build --no-cache . -t projet_final/api_historic:0.0.1

cd ./../up

docker-compose up -d