import modules.Database as database
import os

if __name__=='__main__':
    #codigo main
    try:
        POSTGRES_USER=os.environ.get('POSTGRES_USER')
        POSTGRES_PASSWORD=os.environ.get('POSTGRES_PASSWORD')
        POSTGRES_DB=os.environ.get('POSTGRES_DB')
        try:
            db = database.Database(POSTGRES_USER,POSTGRES_PASSWORD,"postgres","5432",POSTGRES_DB)
            db.print()
        except:
            print("Error connecting to the database")
    except:
        print("Error getting environement variables")
