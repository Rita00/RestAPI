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
            'participant',
            'person_username, person_email, person_password',
            f"'{content['username']}', '{content['email']}', '{content['password']}'",
            'person_id',
            f"person_username='{content['username']}'"
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
        person_id = db.select("person_id", 'participant', f'person_username={username}')
        # insere o leilão
        id = db.insert(
            'auction',
            'code, min_price, begin_date, end_date, participant_person_id',
            f"{content['artigoId']}, {content['precoMinimo']}, '{content['password']}',{person_id}",
            'person_id',
            f"person_username='{content['username']}'"
        )
        # conta as versoes existentes
        version = db.select("count(*)", 'textual_description', f'auction_id={id}') + 1
        # insere os dados textuais do leilão
        db.insert(
            'textual_description',
            'version, title, description, alteration_date, auction_id',
            f"{version},'{content['titulo']}', '{content['descricao']}', NOW(),{id}",
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
