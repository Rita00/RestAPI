import modules.Database as database
import os

if __name__=='__main__':
    #codigo main
    try:
        POSTGRES_USER=os.environ.get('POSTGRES_USER')
        POSTGRES_PASSWORD=os.environ.get('POSTGRES_PASSWORD')
        POSTGRES_DB=os.environ.get('POSTGRES_DB')
        print("User: ",POSTGRES_USER)
        print("Password: ***")
        print("DB: ",POSTGRES_DB)
    except:
        print("Error getting environement variables")
    db = database.Database(POSTGRES_USER,POSTGRES_PASSWORD,"postgres","5432",POSTGRES_DB)
    db.print()