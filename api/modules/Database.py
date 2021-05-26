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

    def insert(self, sql, return_sql=None):
        """ Insere na base de dados"""
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        if (return_sql != None):
            cursor.execute(return_sql)
        res = cursor.fetchone()[0]
        cursor.close()
        return res

    def selectOne(self, sql):
        """ Seleciona na base de dados"""
        cursor = self.connection.cursor()
        cursor.execute(sql)
        res = cursor.fetchone()[0]
        cursor.close()
        return res

    def selectAll(self,sql):
        """ Seleciona na base de dados"""
        cursor = self.connection.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
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
        # Exemplo de sql injection
        # password1 = '\' union select * from participant WHERE \'1\'= \'1'
        sql = 'SELECT * FROM participant WHERE person_username = %s AND person_password = %s'
        cursor.execute(sql, (username, password))
        if cursor.rowcount < 1:
            cursor.close()

            return False
            #return 'AuthError'

        cursor.close()
        return True

    def listAuctions(self, param):
        cursor = self.connection.cursor()
        sql = 'SELECT id, description FROM auction, textual_description WHERE auction.id = textual_description.auction_id AND (auction.code::text = %s OR textual_description.description like %s)'
        cursor.execute(sql, (param, '%' + param + '%'))
        if cursor.rowcount < 1:
            res = []
        else:
            res = [{"leilaoId": row[0], "descricao": row[1]} for row in cursor.fetchall()]
        cursor.close()
        return res

    def detailsAuction(self, auction_id):
        cursor = self.connection.cursor()
        sqlAuction = 'SELECT id, end_date, description FROM auction, textual_description WHERE auction.id = textual_description.auction_id AND id = %s'
        cursor.execute(sqlAuction, (auction_id, ))
        if cursor.rowcount < 1:
            res = []
        else:
            row = cursor.fetchone()
            res = {"leilãoId": row[0], "dataFim": row[1], "descricao": row[2]}
            sqlMessages = 'SELECT message_id, message_message FROM feed_message WHERE auction_id = %s'
            cursor.execute(sqlMessages, (auction_id, ))
            res['mensagens'] = [{"mensagemId": row[0], "mensagem": row[1]} for row in cursor.fetchall()]
            sqlBids = 'SELECT id, person_username FROM bid, participant WHERE bid.participant_person_id = participant.person_id AND auction_id = %s'
            cursor.execute(sqlBids, (auction_id, ))
            res['licitacoes'] = [{"licitacaoId": row[0], "nomePessoa": row[1]} for row in cursor.fetchall()]
        return res


if __name__ == '__main__':
    # testar codigo desta classe aqui
    db = Database("bidyourauction", "bidyourauction", "docker.for.mac.localhost", "5432", "bidyourauction_db")
    db.print()
