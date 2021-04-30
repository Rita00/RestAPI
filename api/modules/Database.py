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

    def signUp(self, username,email,password,token):
        cursor = self.connection.cursor()
        cursor.execute(
            f"""
            INSERT INTO participant(person_username,person_email,person_password,person_token)
            VALUES ('{username}','{email}','{password}','{token}');
            """
        )
        self.connection.commit()
        cursor.execute(f"SELECT person_id FROM participant WHERE person_username='{username}';")
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


if __name__ == '__main__':
    # testar codigo desta classe aqui
    db = Database("bidyourauction", "bidyourauction", "localhost", "5432", "bidyourauction_db")
    db.print()
