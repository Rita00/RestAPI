import importlib

database = importlib.import_module('modules.Database')

if __name__=='__main__':
    #codigo main
    db = database.Database("project","project","127.0.0.1","7000","project_db")
    db.print()