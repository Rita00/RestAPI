# imports
from re import A
from flask import Flask, request, jsonify
import datetime
import jwt
from functools import wraps
import platform
import os
import random
# custom modules
import modules.Database as database

# config
global db
app = Flask(__name__)

def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            b'\x13\xfc\xe2\x92\x0eE4\xd2\x92\xdd\xd4\x11np\xc8\x0c+<\xb1\xe8i\xf0\xc4O',
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(f):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    @wraps(f)   #why? -> https://www.geeksforgeeks.org/python-functools-wraps-function/
    def inner(*args, **kwargs):

        if 'authToken' not in request.headers or not request.headers['authToken']:
            return jsonify({'erro': 401, 'message' : 'Token is missing!!!'})
            
        
        authToken = request.headers['authToken']

        try:
            payload = jwt.decode(
                authToken,
                b'\x13\xfc\xe2\x92\x0eE4\xd2\x92\xdd\xd4\x11np\xc8\x0c+<\xb1\xe8i\xf0\xc4O',
                algorithm='HS256'
            )
            username = payload['sub']
        except jwt.ExpiredSignatureError:
            return jsonify({'erro': 401, 'message' : 'Signature expired. Please log in again.'})

        except jwt.InvalidTokenError:
            return jsonify({'erro': 401, 'message' : 'Invalid token. Please log in again.'}) 

        return f(username, *args, **kwargs)

    return inner


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
        if db.signIn(content['username'], content['password']):
            token = encode_auth_token(content['username'])
            return jsonify({'authToken': token})

        #wrong credentials
        return jsonify({'erro': 401, 'message': 'Wrong credentials'})

    except Exception as e:
        print(e)
        return jsonify({'erro': 401, 'message': e})
   


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
        version = 1 + db.selectOne(
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

@app.route('/dbproj/leiloes', methods=['GET'])
def listAllAuctions():
    """Listar Todos os leilões existentes"""
    try:
        auctions = db.listAllAuctions()
    except Exception as e:
        print(e)
        return jsonify({'erro': 401})
    return jsonify(auctions)

@app.route('/dbproj/leiloes/<keyword>', methods=['GET'])
def listCurrentAuctions(keyword):
    """Listar os leilões que estão a decorrer"""
    try:
        auctions = db.listAuctions(keyword)
    except Exception as e:
        print(e)
        return jsonify({'erro': 401})
    return jsonify(auctions)


@app.route(f'/dbproj/user/<userId>/leiloes', methods=['GET'])  # TODO username
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
        db.connection.rollback()
        print(e)
        return jsonify({'erro': 401})
    return jsonify(auctions)  # TODO ajeitar isto


@app.route(f'/dbproj/licitar/<leilaoId>/<licictacao>', methods=['POST'])  # TODO leilaoId
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


@app.route('/dbproj/leilao/<leilaoId>', methods=['GET'])
def detailsAuction(leilaoId):
    """Consultar os detalhes de um determinado leilão"""
    try:
        details = db.detailsAuction(leilaoId)
    except Exception as e:
        print(e)
        return jsonify({'erro': 401})
    return jsonify(details)


@app.route('/')
@app.route('/home')
def home():
    return "<h1><center>BidYourAuction<center></h1>"


if __name__ == '__main__':
    '''
    BIDYOURAUCTION_USER = os.environ.get('BIDYOURAUCTION_USER')
    BIDYOURAUCTION_PASSWORD = os.environ.get('BIDYOURAUCTION_PASSWORD')
    BIDYOURAUCTION_HOST = os.environ.get('BIDYOURAUCTION_HOST')
    BIDYOURAUCTION_PORT = os.environ.get('BIDYOURAUCTION_PORT')
    BIDYOURAUCTION_DB = os.environ.get('BIDYOURAUCTION_DB')
    '''

    BIDYOURAUCTION_HOST = "ec2-34-254-69-72.eu-west-1.compute.amazonaws.com"
    BIDYOURAUCTION_PORT = "5432"
    BIDYOURAUCTION_DB = "das7ket3c5aarn"
    BIDYOURAUCTION_PASSWORD = "eb4ada6829ffce0e0f516062ea258ca6aa14d2fd85ea907ad910aa62eaf1412a"
    BIDYOURAUCTION_USER = "vtxuzrplfviiht"
    

    print(BIDYOURAUCTION_USER, BIDYOURAUCTION_PASSWORD, BIDYOURAUCTION_HOST, BIDYOURAUCTION_PORT, BIDYOURAUCTION_DB)
    db = database.Database(
        user=BIDYOURAUCTION_USER,
        password=BIDYOURAUCTION_PASSWORD,
        host=BIDYOURAUCTION_HOST,
        port=BIDYOURAUCTION_PORT,
        database=BIDYOURAUCTION_DB
    )
    app.run(debug=True, host='localhost', port=8080)
