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
                        """, (username,))
        person_id = cursor.fetchone()[0]
        # insere o leilão
        cursor.execute("""
                        INSERT INTO auction(code, min_price, begin_date, end_date, participant_person_id)
                        VALUES (%s,%s,NOW(),%s,%s);
                        """, (article_id, min_price, end_date, person_id))
        cursor.execute("""
                        SELECT id
                        FROM auction
                        WHERE code= %s;
                        """, (article_id,))
        id = cursor.fetchone()[0]
        # conta as versoes existentes
        cursor.execute("""
                        SELECT count(*)
                        FROM textual_description
                        WHERE auction_id=%s;
                        """, (id,))
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
                        """, (username,))
        if cursor.rowcount < 1:
            res = []
        else:
            res = [{"leilaoId": row[0], "descricao": row[1]} for row in cursor.fetchall()]
        cursor.close()
        return res

    def bid(self, username, auction_id, price):
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
                        """, (username,))
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
                        """, (person_id,))
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
                        VALUES(%s,%s,%s,%s,%s);
                        """, (message_type, person_id, auction_id, message, 'NOW()'))

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
        """
                Efetuar login na aplicação

                :param username: nome de utilizador
                :param password: password do utilizador

                :return: true caso o user exista na base de dados, false caso contrário e banned caso o utilizador esteja banido
                """
        cursor = self.connection.cursor()
        # Exemplo de sql injection
        # password1 = '\' union select * from participant WHERE \'1\'= \'1'

        sql = """   
                SELECT * 
                FROM participant
                WHERE (person_username = %s AND person_password = %s) 
            """
        cursor.execute(sql, (username, password))
        if cursor.rowcount < 1:
            sql = """   
                    SELECT * 
                    FROM admin
                    WHERE (person_username = %s AND person_password = %s) 
                """
            cursor.execute(sql, (username, password))
            if cursor.rowcount < 1:
                cursor.close()
                return False
                # return 'AuthError'
            cursor.close()
            return True

        isBanned = 'SELECT isbanned FROM participant WHERE person_username = %s'
        cursor.execute(isBanned, (username,))
        isBanned = cursor.fetchone()[0]
        if isBanned:
            cursor.close()
            return 'banned'
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
        sql = 'SELECT id, description FROM auction, textual_description WHERE auction.id = textual_description.auction_id AND (auction.code::text = %s OR textual_description.description like %s) AND end_date > %s'
        cursor.execute(sql, (param, '%' + param + '%', 'now()'))
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
        cursor.close()
        return res

    def editAuction(self, auction_id, title, description, username):
        cursor = self.connection.cursor()
        # Check if username is the creator of auction
        isCreator = 'SELECT * FROM auction JOIN participant on auction.participant_person_id = participant.person_id AND participant.person_username = %s AND auction.id = %s'
        cursor.execute(isCreator, (username, auction_id))
        if cursor.rowcount < 1:
            cursor.close()
            return "notCreator"

        getLastVersion = 'SELECT count(*) FROM textual_description WHERE auction_id = %s'
        cursor.execute(getLastVersion, (auction_id,))
        lastVersion = cursor.fetchone()[0] + 1
        lastVersion = lastVersion + 1
        sqlAuction = 'INSERT INTO textual_description(version, title, description, alteration_date, auction_id) VALUES(%s, %s, %s, %s, %s)'
        cursor.execute(sqlAuction, (lastVersion, title, description, 'now()', auction_id))

        # Error on insert
        if cursor.rowcount < 1:
            cursor.close()
            return False
        self.connection.commit()

        # Get complete information about auction
        auctionInfo = 'SELECT id, code, min_price, begin_date, end_date, isactive, person_username, title, description FROM auction, participant, textual_description WHERE auction.participant_person_id = participant.person_id AND auction.id = textual_description.auction_id AND auction.id = %s AND textual_description.version = %s'
        cursor.execute(auctionInfo, (auction_id, lastVersion))
        row = cursor.fetchone()
        cursor.close()
        res = {"leilãoId": row[0], "codigo": row[1], "precoMin": row[2], "DataIni": row[3], "DataFim": row[4],
               "Ativo": row[5], "Criador": row[6], "Titulo": row[7], "Descricao": row[8]}
        return res

    def finishAuctions(self):
        # calls a procedure for efficiency
        cursor = self.connection.cursor()
        cursor.execute("CALL finish_auctions();")
        cursor.close()
        return True

    def ban(self, admin, user):
        """
        Banir utilizador definitivamente por um admin.\n
        A adição de dados na tabela admin_participant vai ativar um trigger
        que encarrega-se de atualizar os dados todas das restantes tabelas devidas ao
        baniamento do utilizador.

        :param admin: administrador
        :param user: utilizador banido

        :return: id do administrador e do utilizador que foi banido por ele
        """
        cursor = self.connection.cursor()
        # buscar id do admin
        cursor.execute("""
                        SELECT person_id
                        FROM admin
                        WHERE person_username=%s;
                        """, (admin,))
        admin_id = cursor.fetchone()[0]
        # buscar id do participante
        cursor.execute("""
                        SELECT person_id
                        FROM participant
                        WHERE person_username=%s;
                        """, (user,))
        user_id = cursor.fetchone()[0]
        # registar a mensagem
        cursor.execute("""
                        INSERT INTO admin_participant
                        VALUES(%s,%s);
                        """, (admin_id, user_id))
        cursor.close()
        self.connection.commit()
        return admin_id, user_id


if __name__ == '__main__':
    # testar codigo desta classe aqui
    db = Database("bidyourauction", "bidyourauction", "docker.for.mac.localhost", "5432", "bidyourauction_db")
    db.print()
