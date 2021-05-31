# imports
from re import A
from flask import Flask, request, jsonify
import datetime
import jwt
from functools import wraps
from cryptography.fernet import Fernet
import platform
import os
import random
# custom modules
import modules.Database as database
import modules.Utils as utils

# config
global db
global f
app = Flask(__name__)


def generate_token(user_id):
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
            app.config.get('SECRET'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


def verify_token(f):
    """
    Decodes the auth token

    :param f:

    :return: integer|string
    """

    @wraps(f)  # why? -> https://www.geeksforgeeks.org/python-functools-wraps-function/
    def inner(*args, **kwargs):

        if 'Token' not in request.headers or not request.headers['Token']:
            return jsonify({'erro': 401, 'message': 'Token is missing!!!'})

        authToken = request.headers['Token']

        try:
            payload = jwt.decode(
                authToken,
                app.config.get('SECRET'),
                algorithms=['HS256']
            )
            username = payload['sub']
        except jwt.ExpiredSignatureError:
            return jsonify({'erro': 401, 'message': 'Signature expired. Please log in again.'})

        except jwt.InvalidTokenError:
            return jsonify({'erro': 401, 'message': 'Invalid token. Please log in again.'})

        return f(username, *args, **kwargs)

    return inner


@app.route('/dbproj/user', methods=['POST'])
def signUp():
    """
    Registar um utilizador

    :return: resposta da request
    """
    id = None
    try:
        content = request.json
        valid = utils.validateTypes(content, [str, str, str])
        valid = valid & utils.isemail(content['email'])
        if not valid:
            return jsonify({'erro': 404})
        enc = f.encrypt(content['password'].encode())
        id = db.signUp(content['username'], content['email'], enc.decode())
        db.connection.commit()

        print(f"Added user #{id}")
        return jsonify({'userId': id})
    except Exception as e:
        db.connection.rollback()
        print(e)
        return jsonify({'erro': 401})


@app.route('/dbproj/user', methods=['PUT'])
def signIn():
    """Login do utilizador"""
    try:
        content = request.json
        valid = utils.validateTypes(content, [str, str])
        if not valid:
            return jsonify({'erro': 404})
        correctSignIn = db.signIn(content['username'])
        db.connection.commit()
        if correctSignIn[0]:
            decoded = f.decrypt(correctSignIn[1].encode()).decode()
            if correctSignIn[0] == True and content['password'] == decoded:
                token = generate_token(content['username'])

                return jsonify({'authToken': token})

            # Is Banned
            elif 'banned' == correctSignIn[1]:
                return jsonify({'erro': 'User is banned'})
        # wrong credentials
        return jsonify({'erro': 401, 'message': 'Wrong credentials'})

    except Exception as e:
        db.connection.rollback()
        print(e)
        return jsonify({'erro': 401, 'message': e})


@app.route('/dbproj/leilao', methods=['POST'])
@verify_token
def createAuction(username):
    """Criar Leilão"""
    id = None
    try:
        content = request.json
        valid = utils.validateTypes([username], [str])
        valid = valid & utils.validateTypes(content, [int, float, str, str, str])
        valid = valid & utils.validateDates([content['dataFim']])
        if not valid:
            return jsonify({'erro': 404})
        id = db.createAuction(username, content['artigoId'], content['precoMinimo'],
                              content['dataFim'], content['titulo'], content['descricao'])
        db.connection.commit()
        print(f"Added auction #{id}")
        return jsonify({'leilãoId': id})
    except Exception as e:
        db.connection.rollback()
        print(e)
        return jsonify({'erro': 401})


@app.route('/dbproj/leiloes', methods=['GET'])
@verify_token
def listAllAuctions(username):
    """Listar Todos os leilões existentes que estão a decorrer"""
    try:
        auctions = db.listAllAuctions()
        db.connection.commit()
        return jsonify(auctions)
    except Exception as e:
        db.connection.rollback()
        print(e)
        return jsonify({'erro': 401})


@app.route('/dbproj/leiloes/<keyword>', methods=['GET'])
@verify_token
def listCurrentAuctionsByKeyword(username, keyword):
    """Listar os leilões que estão a decorrer"""
    try:
        valid = utils.validateTypes([keyword], [str])
        if not valid:
            return jsonify({'erro': 404})
        auctions = db.listAuctions(keyword)
        if auctions == "noResults":
            db.connection.commit()
            return jsonify({'Ups': 'Sem resultados para esta pesquisa!'})
        db.connection.commit()
        return jsonify(auctions)
    except Exception as e:
        db.connection.rollback()
        print(e)
        return jsonify({'erro': 401})


@app.route(f'/dbproj/user/leiloes', methods=['GET'])
@verify_token
def listUserAuctions(username):
    """Listar os leilões em que o utilizador tenha uma atividade"""
    try:
        valid = utils.validateTypes([username], [str])
        if not valid:
            return jsonify({'erro': 404})
        auctions = db.listUserAuctions(username)
        db.connection.commit()
        return jsonify(auctions)  # TODO ajeitar isto
    except Exception as e:
        db.connection.rollback()
        print(e)
        return jsonify({'erro': 401})


@app.route(f'/dbproj/licitar/<leilaoId>/<licictacao>', methods=['POST'])  # TODO leilaoId
@verify_token
def bid(username, leilaoId, licictacao):
    """Listar os leilões em que o utilizador tenha uma atividade"""
    try:
        valid = utils.validateTypes([username, leilaoId, licictacao], [str, int, float])
        if not valid:
            return jsonify({'erro': 404})
        bid_id = db.bid(username, leilaoId, licictacao)
        db.connection.commit()
        if bid_id == 'inactive':
            return jsonify({'erro': 'O leilão está inativo.'})
        if bid_id == 'noAuction':
            return jsonify({'erro': 'O leilão não existe.'})
        if bid_id == 'lowPrice':
            return jsonify({'erro': 'Licitação demasiado baixa.'})
        return jsonify({'licitacaoId': bid_id})
    except Exception as e:
        db.connection.rollback()
        print(e)
        return jsonify({'erro': 401})


@app.route('/dbproj/leilao/<leilaoId>', methods=['GET'])
@verify_token
def detailsAuction(username, leilaoId):
    """Consultar os detalhes de um determinado leilão"""
    try:
        valid = utils.validateTypes([leilaoId], [int])
        if not valid:
            return jsonify({'erro': 404})
        details = db.detailsAuction(leilaoId)
        db.connection.commit()
        if details == "noAuction":
            return jsonify({'erro': 'O leilão não existe!'})
        return jsonify(details)
    except Exception as e:
        db.connection.rollback()
        print(e)
        return jsonify({'erro': 401})


@app.route('/dbproj/feed/<leilaoId>', methods=['POST'])
@verify_token
def writeFeedMessage(username, leilaoId):
    """Escrever mensagem no mural de um leilão"""
    try:
        content = request.json
        valid = utils.validateTypes([username, leilaoId], [str, int])
        valid = valid & utils.validateTypes(content, [str, str])
        if not valid:
            return jsonify({'erro': 404})
        message_id = db.writeFeedMessage(username, leilaoId, content["message"], content["type"])
        db.connection.commit()

        if message_id == "noAuction":
            return jsonify({'erro': 'O leilão não existe!'})
        if message_id == "cancelled":
            return jsonify({'erro': 'O leilão não está ativo, não pode escrever mensagens!'})

        return jsonify({'messageId': message_id})
    except Exception as e:
        db.connection.rollback()
        print(e)
        return jsonify({'erro': 401})


@app.route('/dbproj/leilao/edit/<leilaoId>', methods=['PUT'])
@verify_token
def editAuction(username, leilaoId):
    """Editar propriedades de um leilão"""
    try:
        content = request.json
        valid = utils.validateTypes([username, leilaoId], [str, int])
        valid = valid & utils.validateTypes(content, [str, str])
        if not valid:
            return jsonify({'erro': 404})
        res = db.editAuction(leilaoId, content["titulo"], content["descricao"], username)
        db.connection.commit()
        if res == "notCreator":
            return jsonify({'erro': "Não é o criador do leilão, não o pode editar!"})
        if res == "noAuction":
            return jsonify({'erro': 'O leilão não existe!'})
        # Error on insert
        elif not res:
            return jsonify({'erro': 401})
        return jsonify(res)
    except Exception as e:
        db.connection.rollback()
        print(e)
        return jsonify({'erro': 401})


@app.route('/dbproj/inbox', methods=['GET'])
@verify_token
def getNotifications(username):
    """Listar todas as notificações da mais recente para a mais antiga"""
    try:
        valid = utils.validateTypes([username], [str])
        if not valid:
            return jsonify({'erro': 404})
        notifications = db.listNotifications(username)
        db.connection.commit()
        return jsonify(notifications)
    except Exception as e:
        db.connection.rollback()
        print(e)
        return jsonify({'erro': 401})


@app.route('/dbproj/leilao/checkFinish', methods=['PUT'])
def finishAuction():
    """Terminar leilão na data, hora e minuto marcados"""
    try:
        db.finishAuctions()
        db.connection.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        db.connection.rollback()
        print(e)
        return jsonify({'erro': 401})


########## ADMIN ##########

@app.route('/dbproj/ban/<user>', methods=['PUT'])
@verify_token
def ban(username, user):
    """Banir um utilizador definitivamente"""
    try:
        valid = utils.validateTypes([username, user], [str, str])
        if not valid:
            return jsonify({'erro': 404})
        admin_id, user_id = db.ban(username, user)
        db.connection.commit()
        return jsonify({'adminId': admin_id, 'userId': user_id})
    except Exception as e:
        db.connection.rollback()
        print(e)
        return jsonify({'erro': 401})


@app.route('/dbproj/leilao/cancel/<leilaoId>', methods=['PUT'])
@verify_token
def cancelAuction(username, leilaoId):
    """Um administrador pode cancelar um leilão"""
    try:
        valid = utils.validateTypes([username, leilaoId], [str, int])
        if not valid:
            return jsonify({'erro': 404})
        res = db.cancelAuction(leilaoId, username)
        db.connection.commit()
        if res == "notAdmin":
            return jsonify({'erro': "Sem permissões de administrador!"})
        elif res == "noAuction":
            return jsonify({'erro': "O leilão não existe!"})
        elif res == "cancelled":
            return jsonify({'erro': "O leilão já está cancelado!"})
        elif res == "inactive":
            return jsonify({'erro': 'O leilão está terminado, impossível cancelar!'})
        else:
            return jsonify(res)
    except Exception as e:
        db.connection.rollback()
        print(e)
        return jsonify({'erro': 401})


@app.route('/dbproj/stats', methods=['GET'])
@verify_token
def stats(username):
    """
    Consultar estatisticas da applicação: \n
    - TOP10 utilizadores com mais leilões criados \n
    - TOP10 utilizadores que mais leilões venceram |n
    - número total de leilões nos últimos 10 dias

    :param username: username do administrador

    :return: resposta
    """
    try:
        valid = utils.validateTypes([username], [str])
        if not valid:
            return jsonify({'erro': 404})
        res = db.stats(username)
        db.connection.commit()
        return jsonify({'topCriadores': res[0], 'topVencedores': res[1], 'numeroDeLeiloesNosUltimosDezDias': res[2]})
    except Exception as e:
        db.connection.rollback()
        print(e)
        return jsonify({'erro': 401})


@app.route('/*')
def home():
    """
    Devolve page not found error

    :return: codigo de erro
    """
    return jsonify({'erro': 404})


if __name__ == '__main__':
    BIDYOURAUCTION_USER = os.environ.get('BIDYOURAUCTION_USER')
    BIDYOURAUCTION_PASSWORD = os.environ.get('BIDYOURAUCTION_PASSWORD')
    BIDYOURAUCTION_HOST = os.environ.get('BIDYOURAUCTION_HOST')
    BIDYOURAUCTION_PORT = os.environ.get('BIDYOURAUCTION_PORT')
    BIDYOURAUCTION_DB = os.environ.get('BIDYOURAUCTION_DB')
    
    SECRET = os.environ.get('SECRET')
    KEY = os.environ.get('KEY')

    f = Fernet(KEY.encode())

    app.config['SECRET'] = SECRET.encode()

    db = database.Database(
        user=BIDYOURAUCTION_USER,
        password=BIDYOURAUCTION_PASSWORD,
        host=BIDYOURAUCTION_HOST,
        port=BIDYOURAUCTION_PORT,
        database=BIDYOURAUCTION_DB
    )
    app.run(debug=True, host='localhost', port=8080)
