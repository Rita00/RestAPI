import psycopg2


class Database(object):
    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.connect()

    def connect(self):
        self.connection = psycopg2.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database
        )


    def insert(self, table, columns, values, returnVal, returnCond):
        """ Insere na base de dados"""
        cursor = self.connection.cursor()
        cursor.execute(
            f"""
            INSERT INTO {table}({columns})
            VALUES ({values});
            """
        )
        self.connection.commit()
        if(returnVal!=None):
            cursor.execute(f"SELECT {returnVal} FROM {table} WHERE {returnCond};")
        res = cursor.fetchone()[0]
        cursor.close()
        return res

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

    def signIn(self, username, password):
        cursor = self.connection.cursor()
        cursor.execute(f"""
        SELECT * FROM participant WHERE person_username = '{username}' AND person_password = '{password}'""")
        res = cursor.fetchall()[0]
        cursor.close()
        if res is None:
            return 'AuthError'
        return ''


if __name__ == '__main__':
    # testar codigo desta classe aqui
    db = Database("bidyourauction", "bidyourauction", "docker.for.mac.localhost", "5432", "bidyourauction_db")
    db.print()
