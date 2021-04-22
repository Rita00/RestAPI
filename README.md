# BidYourAuction
## Build the volume container
```shell
sh docker-compose.sh
```
or
```shell
bash docker-compose.sh
```
It will create the database and runs the server
## Connect to database
```shell
psql -h localhost -p 5432 -d bidyourauction_db -U bidyourauction -w bidyourauction
```
