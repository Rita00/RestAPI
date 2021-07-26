# BidYourAuction

## Setup
### Requirements
1. PostgreSQL
2. Python 3.9
3. Libraries & Frameworks
```shell
python -m pip install wheel
python -m pip install flask
python -m pip install jwt
python -m pip install psycopg2
python -m pip install cryptography
```
### Connect to database
```shell
psql -h localhost -p 5432 -d postgres -U postgres
```
### Database Setup
1. Connect to the database
```shell
psql -h <host> -p <port> -d <db_name> -U <user>
```
2. Insert password
```shell
<password>
```
3. Execute *data.sql*
```pgplsql
\i data.sql;
```
## Register admins
1. Modify *registAdmins.py*
```python
# [ [username, password, email], ... ]
admins = [
    ["username1", "password1", "e@mail1.com"],
    ["username2", "password2", "e@mail2.com"],
    ...
]
```
2. Execute Script
```shell
python3 registAdmins.py
```
## Requests
### User Sign Up
```apache
POST http://localhost:8080/dbproj/user
```
```yaml
{
   "username": "maria",
   "email": "maria@email.com",
   "password": "password"
}
```
### Sign In
```apache
PUT http://localhost:8080/dbproj/user
```
```yaml
{
   "username": "mara",
   "password": "password"
}
```
### Create Auction
```apache
POST http://localhost:8080/dbproj/leilao
```
```yaml
{
   "artigoId": 69,
   "precoMinimo": 10000.00,
   "titulo": "Lingote de ouro",
   "descricao": "Ouro puro (24 quilates)",
   "dataFim": "2021-06-10 23:59"
}
```
### List existing Auctions
```apache
GET http://localhost:8080/dbproj/leiloes
```
### Search existing Auctions
```apache
GET http://localhost:8080/dbproj/leiloes/{keyword}
```
### Auction's details 
```apache
GET http://localhost:8080/dbproj/leilao/{leilaoId}
```
### List Auctions where user has some activity
```apache
GET http://localhost:8080/dbproj/user/leiloes
```
### Bid
```apache
POST http://localhost:8080/dbproj/licitar/{leilaoId}/{licitacao}
```
### Edit Auction's details
```apache
PUT http://localhost:8080/dbproj/leilao/{leilaoId}
```
```yaml
{
   "titulo": "Agua do Mondegoo",
   "descricao": "Agua fresca do rio Mondegoo"
}
```
### Write feed message
```apache
POST http://localhost:8080/dbproj/feed/{leilaoId}
```
```yaml
{
   "message": "O que justifica o preco do artigo?",
   "type": "question"
}
```
### List notifications
```apache
GET http://localhost:8080/dbproj/inbox
```
### Check if Auction ended
```apache
PUT http://localhost:8080/dbproj/leilao/checkFinish
```
### Cancel Auction
```apache
PUT http://localhost:8080/dbproj/leilao/cancel/{leilaoId}
```
### Ban user
```apache
PUT http://localhost:8080/dbproj/ban/{username}
```
### Get some statistics
```apache
GET http://localhost:8080/dbproj/stats
```
