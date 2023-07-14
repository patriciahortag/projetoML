### Execute os comando em sequencia

docker network create meli_network

docker-compose up

docker run -d --name mysql_container --network meli_network -e MYSQL_ROOT_PASSWORD=ehcQ8jpfjrGST93n -p 3306:3306 mysql:latest

docker build -t mlchallenge_image .

docker run -d --name mlchallenge_container --network meli_network mlchallenge_image:latest

docker run -d --name mlchallenge_container --network meli_network mlchallenge_image:latest



### obter informações sobre a rede
docker network inspect meli_network
