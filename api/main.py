# imports
from flask import Flask, request, jsonify
import jwt
import platform
import os
import random
# custom modules
import modules.Database as database

# config
global db
app = Flask(__name__)


@app.route('/dbproj/user', methods=['POST'])
def signUp():
    """Registar um utilizador"""
    id = None
    try:
        content = request.json
        id = db.insert(
            f"""
            INSERT INTO participant (person_username, person_email, person_password)
            VALUES '{content['username']}', '{content['email']}', '{content['password']}';
            """,
            f"""
            SELECT person_id
            FROM participant
            WHERE person_username='{content['username']}';
            """
        )
    except Exception as e:
        db.connection.rollback()
        print(e)
        return jsonify({'erro': 401})
    print(f"Added user #{id}")
    return jsonify({'userId': id})


@app.route('/dbproj/user', methods=['PUT'])
def signIn():
    """Login do utilizador"""
    try:
        content = request.json
        authToken = db.signIn(content['username'], content['password'])
    except Exception as e:
        print(e)
        return jsonify({'erro': 401})
    return jsonify({'authToken': authToken})


@app.route('/dbproj/leilao', methods=['POST'])
def createAuction(username):
    """Criar Leilão"""
    id = None
    try:
        content = request.json
        # vai buscar o criador da eleição
        person_id = db.selectOne(
            f"""
            SELECT person_id
            FROM participant
            WHERE person_username={username};
            """
        )
        # insere o leilão
        id = db.insert(
            f"""
            INSERT INTO auction(code, min_price, begin_date, end_date, participant_person_id)
            VALUES ({content['artigoId']}, {content['precoMinimo']},'{content['dataInicio']}','{content['dataFim']}',{person_id});
            """,
            f"""
            SELECT id
            FROM auction
            WHERE code={content['artigoId']};
            """
        )
        # conta as versoes existentes
        version = 1+db.selectOne(
            f"""
            SELECT count(*)
            FROM textual_description
            WHERE auction_id={id};
            """
        )
        # insere os dados textuais do leilão
        db.insert(
            f"""
            INSERT INTO textual_description(version, title, description, alteration_date, auction_id)
            VALUES ({version},'{content['titulo']}', '{content['descricao']}', NOW(),{id});
            """
        )
    except Exception as e:
        db.connection.commit()
        print(e)
        return jsonify({'erro': 401})
    print(f"Added user #{id}")
    return jsonify({'leilãoId': id})


@app.route('/dbproj/leiloes/<keyword>', methods=['GET'])
def listCurrentAuctions(keyword):
    """Listar os leilões que estão a decorrer"""
    try:
        auctions = db.listAuctions(keyword)
    except Exception as e:
        print(e)
        return jsonify({'erro': 401})
    return jsonify(auctions)

@app.route(f'/dbproj/user/<userId>/leiloes', methods=['GET'])        #TODO username
def listUserAuctions(username):
    """Listar os leilões em que o utilizador tenha uma atividade"""
    try:
        auctions = db.selectAll(
            f"""
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
                        WHERE p.person_username LIKE '{username}'
                    )
                )
            );
            """
        )
    except Exception as e:
        print(e)
        return jsonify({'erro': 401})
    return jsonify(auctions) #TODO ajeitar isto

@app.route(f'/dbproj/licitar/<leilaoId>/<licictacao>', methods=['POST'])        #TODO leilaoId
def bid(username, auctionID, price):
    """Listar os leilões em que o utilizador tenha uma atividade"""
    try:
        person_id = db.selectOne(
            f"""
            SELECT person_id
            FROM participant
            WHERE person_username={username};
            """
        )
        person_bid = db.insert(
            f"""
            INSERT INTO bid(bid_date, price, participant_person_id, auction_id)
            VALUES(now(),{price},{person_id},{auctionID});
            """,
            f"""
            SELECT b.id
            FROM bid b, participant p
            WHERE b.participant_person_id={person_id}
            ORDER BY b.bid_date DESC;
            """
        )
    except Exception as e:
        print(e)
        return jsonify({'erro': 401})
    return jsonify({'licitacaoId': person_bid})

@app.route('/')
@app.route('/home')
def home():
    return "<h1><center>BidYourAuction<center></h1>"


if __name__ == '__main__':
    BIDYOURAUCTION_USER = os.environ.get('BIDYOURAUCTION_USER')
    BIDYOURAUCTION_PASSWORD = os.environ.get('BIDYOURAUCTION_PASSWORD')
    BIDYOURAUCTION_HOST = os.environ.get('BIDYOURAUCTION_HOST')
    BIDYOURAUCTION_PORT = os.environ.get('BIDYOURAUCTION_PORT')
    BIDYOURAUCTION_DB = os.environ.get('BIDYOURAUCTION_DB')
    print(BIDYOURAUCTION_USER, BIDYOURAUCTION_PASSWORD, BIDYOURAUCTION_HOST, BIDYOURAUCTION_PORT, BIDYOURAUCTION_DB)
    db = database.Database(
        user=BIDYOURAUCTION_USER,
        password=BIDYOURAUCTION_PASSWORD,
        host=BIDYOURAUCTION_HOST,
        port=BIDYOURAUCTION_PORT,
        database=BIDYOURAUCTION_DB
    )
    app.run(debug=True, host='localhost', port=8080)
