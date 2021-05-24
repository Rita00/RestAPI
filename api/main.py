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
        token = random.randint(0, 10000)  # TODO nao é definitivo
        id = db.signUp(content['username'], content['email'], content['password'], token)
    except Exception as e:
        print(e)
        return jsonify({'erro': 401})
    print(f"Added user #{id}")
    return jsonify({'userId': id})


@app.route('/dbproj/user', methods=['PUT'])
def signIn():
    """Login do utilizador"""
    pass


@app.route('/')
@app.route('/home')
def home():
    return "<h1><center>BidYourAuction<center></h1>"


if __name__ == '__main__':
    db_host = None
    if 'Windows' == platform.system():  # windows
        db_host = '127.0.0.1'
        user = 'postgres'
    elif 'Darwin' == platform.system():  # macOS
        db_host = 'docker.for.mac.localhost'
        user = 'bidyourauction'
    else:  # Linux (for docker)
        db_host = 'postgres'
        user = 'bidyourauction'

    # BIDYOURAUCTION_USER=os.environ.get('BIDYOURAUCTION_USER')
    # BIDYOURAUCTION_PASSWORD=os.environ.get('BIDYOURAUCTION_PASSWORD')
    # BIDYOURAUCTION_DB=os.environ.get('BIDYOURAUCTION_DB')
    # db = database.Database(BIDYOURAUCTION_USER,BIDYOURAUCTION_PASSWORD,db_host,"5432",BIDYOURAUCTION_DB)

    db = database.Database(user, user, db_host, "5432", 'bidyourauction_db')
    app.run(debug=True, host='localhost', port=8080)
