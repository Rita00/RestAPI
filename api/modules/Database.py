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

    def print(self):
        print("user = ", self.user)
        print("password = ", self.password)
        print("host = ", self.host)
        print("port = ", self.port)
        print("database = ", self.database)

    def signUp(self, username, email, password):
        """
        Registar um Utilizador

        :param username: nome de utilizador
        :param email: endereço email
        :param password: palavra passe

        :return: id do utilizador criado
        """
        # regista a pessoa
        cursor = self.connection.cursor()
        cursor.execute("""
                        INSERT INTO participant (person_username, person_email, person_password)
                        VALUES (%s,%s,%s);
                        """, (username, email, password))
        # vai buscar o id da pessoa
        cursor.execute("""
                        SELECT person_id
                        FROM participant
                        WHERE person_username = %s;
                        """, (username,))
        res = cursor.fetchone()[0]
        cursor.close()
        self.connection.commit()
        return res

    def createAuction(self, username, article_id, min_price, begin_date, end_date, title, description):
        """
        Insere um leilão na base de dados

        :param username: nome de utilizador
        :param article_id: id do artigo
        :param min_price: preco minimo
        :param begin_date: data de inicio
        :param end_date: data de fim
        :param title: titulo
        :param description: descricao

        :return: id do leilão criado
        """
        # vai buscar o criador da eleição
        cursor = self.connection.cursor()
        cursor.execute("""
                        SELECT person_id
                        FROM participant
                        WHERE person_username=%s;
                        """,tuple(username))
        person_id = cursor.fetchone()[0]
        # insere o leilão
        cursor.execute("""
                        INSERT INTO auction(code, min_price, begin_date, end_date, participant_person_id)
                        VALUES (%s,%s,%s,%s,%s);
                        """, (article_id,min_price, begin_date, end_date, person_id))
        cursor.execute("""
                        SELECT id
                        FROM auction
                        WHERE code= %s;
                        """, tuple(article_id))
        id = cursor.fetchone()[0]
        # conta as versoes existentes
        cursor.execute("""
                        SELECT count(*)
                        FROM textual_description
                        WHERE auction_id=%s;
                        """, tuple(id))
        version = 1 + cursor.fetchone()[0]
        # insere os dados textuais do leilão
        cursor.execute("""
                        INSERT INTO textual_description(version, title, description, alteration_date, auction_id)
                        VALUES (%s,%s,%s, NOW(),%s);
                        """, (version, title, description, id))
        cursor.close()
        self.connection.commit()
        return id

    def listUserAuctions(self, username):
        """
        Lista os leilões em que a pessoa tenha atividade

        :param username: nome de utilizador

        :return: leilões
        """
        cursor = self.connection.cursor()
        cursor.execute("""
                        SELECT t.auction_id, t.description
                        FROM textual_description t
                        WHERE (t.auction_id,t.version) IN (
                            SELECT DISTINCT a.id, MAX(t.version)
                            FROM auction a,
                                 textual_description t
                            WHERE a.id = t.auction_id
                            GROUP BY a.id
                            HAVING a.id IN (
                                SELECT b.auction_id
                                FROM bid b
                                WHERE b.participant_person_id IN (
                                    SELECT p.person_id
                                    FROM participant p
                                    WHERE p.person_username LIKE %s
                                )
                            )
                        );
                        """, tuple(username))
        res = cursor.fetchall()
        cursor.close()
        return res

    def bid(self, username, price, auction_id):
        """
        Efetua uma licitação

        :param username: nome de utilizador
        :param price: preco da licitação
        :param auction_id: id do leilão

        :return: id da licitacao
        """
        cursor = self.connection.cursor()
        # buscar id do participante
        cursor.execute("""
                        SELECT person_id
                        FROM participant
                        WHERE person_username=%s;
                        """, tuple(username))
        person_id = cursor.fetchone()[0]
        # registar a licitacao
        cursor.execute("""
                        INSERT INTO bid(bid_date, price, participant_person_id, auction_id)
                        VALUES(NOW(),%s,%s,%s);
                        """, (price, person_id, auction_id))
        # devolver id da licitacao
        cursor.execute("""
                        SELECT b.id
                        FROM bid b, participant p
                        WHERE b.participant_person_id=%s
                        ORDER BY b.bid_date DESC;
                        """, tuple(person_id))
        bid_id = cursor.fetchone()[0]
        cursor.close()
        self.connection.commit()
        return bid_id

    def writeFeedMessage(self, username, auction_id, message, message_type):
        """
        Escrever uma mensagem no mural de um leilão

        :param username: nome de utilizador
        :param auction_id: id do leilão
        :param message: mensagem
        :param message_type: tipo da mensagem

        :return: id da mensagem
        """
        
        cursor = self.connection.cursor()
        # buscar id do participante
        cursor.execute("""
                        SELECT person_id
                        FROM participant
                        WHERE person_username=%s;
                        """, (username,))
        person_id = cursor.fetchone()[0]
        
        # registar a mensagem
        cursor.execute("""
                        INSERT INTO feed_message(type, participant_person_id, auction_id, message_message, message_message_date)
                        VALUES(%s,%s,%s,%s,NOW());
                        """, (message_type, person_id, auction_id, message))

        # devolver id da mensagem
        cursor.execute("""
                        SELECT m.message_id
                        FROM feed_message m, participant p
                        WHERE m.participant_person_id=%s
                        ORDER BY m.message_message_date DESC;
                        """, (person_id,))
        message_id = cursor.fetchone()[0]
        cursor.close()
        self.connection.commit()
        return message_id

    def signIn(self, username, password):
        cursor = self.connection.cursor()
        # Exemplo de sql injection
        # password1 = '\' union select * from participant WHERE \'1\'= \'1'
        sql = 'SELECT * FROM participant WHERE person_username = %s AND person_password = %s'
        cursor.execute(sql, (username, password))
        if cursor.rowcount < 1:
            cursor.close()

            return False
            # return 'AuthError'

        cursor.close()
        return True

    def listAllAuctions(self):
        cursor = self.connection.cursor()
        sql = 'SELECT id, description FROM auction, textual_description WHERE auction.id = textual_description.auction_id'
        cursor.execute(sql)
        if cursor.rowcount < 1:
            res = []
        else:
            res = [{"leilaoId": row[0], "descricao": row[1]} for row in cursor.fetchall()]
        cursor.close()
        return res

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
        cursor.execute(sqlAuction, (auction_id,))
        if cursor.rowcount < 1:
            res = []
        else:
            row = cursor.fetchone()
            res = {"leilãoId": row[0], "dataFim": row[1], "descricao": row[2]}
            sqlMessages = 'SELECT message_id, message_message FROM feed_message WHERE auction_id = %s'
            cursor.execute(sqlMessages, (auction_id,))
            res['mensagens'] = [{"mensagemId": row[0], "mensagem": row[1]} for row in cursor.fetchall()]
            sqlBids = 'SELECT id, person_username FROM bid, participant WHERE bid.participant_person_id = participant.person_id AND auction_id = %s'
            cursor.execute(sqlBids, (auction_id,))
            res['licitacoes'] = [{"licitacaoId": row[0], "nomePessoa": row[1]} for row in cursor.fetchall()]
        return res


if __name__ == '__main__':
    # testar codigo desta classe aqui
    db = Database("bidyourauction", "bidyourauction", "docker.for.mac.localhost", "5432", "bidyourauction_db")
    db.print()
