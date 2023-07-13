# projetoML

### Execute os comando em sequencia

docker run --name mysql_container -e MYSQL_ROOT_PASSWORD=ehcQ8jpfjrGST93n -p 3306:3306 -d mysql:latest

docker build -t mlchallenge_image .

docker run --name mlchallenge_container mlchallenge_image
