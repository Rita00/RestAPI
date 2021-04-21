import modules.Database as database

if __name__=='__main__':
    #codigo main
    db = database.Database("postgres","postgres","127.0.0.1","8080","bidyourauction_db")
    db.print()
    while True:
        pass