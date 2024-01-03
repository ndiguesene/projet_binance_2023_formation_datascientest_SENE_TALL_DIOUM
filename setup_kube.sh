cd ./models/

kubectl create -f model-api-deployment.yaml
kubectl create -f model-api-service.yaml
kubectl create -f model-api-ingress.yaml

cd ./../populate_base/elasticsearch

kubectl create -f populate_into_elastic_deployment.yaml
kubectl create -f populate_into_elastic_crontab.yaml
