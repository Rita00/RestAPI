# BidYourAuction
## Installation
1. PostgresSQL
```shell
docker pull postgres 

docker run -d -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=postgres postgres 
```
2. pgadmin
```shell
docker pull dpage/pgadmin4 

docker run -d -p 80:80 --name pgadmin -e 'PGADMIN_DEFAULT_EMAIL=email@domain.ext' -e 'PGADMIN_DEFAULT_PASSWORD=postgres' dpage/pgadmin4 
```
3. Main Program
```shell
docker build -t bidyourauction .

docker run -t -d --name BidYourAuction bidyourauction
```
- Note: If needed remove the current container
```shell
docker rm <CONTAINER ID>
```
## Create the database
```shell
psql -h localhost -p 5432 -d postgres -U postgres
create database bidyourauction_db;
```
## Run
On the BidYourAuction container execute the main.py program
```shell
python main.py
```
