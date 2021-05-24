# BidYourAuction

## Local Configuration
### Connect to database
```shell
psql -h localhost -p 5432 -d postgres -U postgres
```
### List all avaliable databases
```psql
\l
```
### Create the Database
```psql
CREATE DATABASE bidyourauction_db
```
### Connect to the Database
```psql
psql -h localhost -p 5432 -d bidyourauction_db -U postgres
```


## Heroku Configuration
```psql
psql -h ec2-34-254-69-72.eu-west-1.compute.amazonaws.com -p 5432 -d das7ket3c5aarn -U vtxuzrplfviiht
```
- Password:
    ```
    eb4ada6829ffce0e0f516062ea258ca6aa14d2fd85ea907ad910aa62eaf1412a
```
