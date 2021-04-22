#Remove todos os contentores a correr
docker rmi -f bd2021_server:latest
docker rmi -f bd2021_database:latest
docker rm -v -f postgres
docker rm -v -f bidyourauction

docker-compose -f docker-compose.yml up --build
