import psycopg2

class Database(object):
    def __init__(self, user,password,host,port,database):
        self.user=user
        self.password=password
        self.host=host
        self.port=port
        self.database=database
        self.connection=None

    def connect(self):
        self.connection = psycopg2.connect(
            user = self.user,
            password = self.password,
            host = self.host,
            port = self.port,
            database = self.database
        )

    def insert(self, sql):
        pass

    def remove(self, sql):
        pass

    def update(self, sql):
        pass

    def print(self):
        print("user = ", self.user)
        print("password = ", self.password)
        print("host = ", self.host)
        print("port = ", self.port)
        print("database = ", self.database)




if __name__=='__main__':
    #testar codigo desta classe aqui
    db = Database("project","project","127.0.0.1","7000","project_db")
    db.print()