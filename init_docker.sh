
docker stop $(docker ps -a -q)
docker rm -v $(docker ps -a -q)

docker rmi -f $(docker images -aq)
