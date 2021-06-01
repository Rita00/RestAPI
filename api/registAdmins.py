# imports
import psycopg2
import os
from cryptography.fernet import Fernet

if __name__ == '__main__':

    
    BIDYOURAUCTION_USER = os.environ.get('BIDYOURAUCTION_USER')
    BIDYOURAUCTION_PASSWORD = os.environ.get('BIDYOURAUCTION_PASSWORD')
    BIDYOURAUCTION_HOST = os.environ.get('BIDYOURAUCTION_HOST')
    BIDYOURAUCTION_PORT = os.environ.get('BIDYOURAUCTION_PORT')
    BIDYOURAUCTION_DB = os.environ.get('BIDYOURAUCTION_DB')
    
    SECRET = os.environ.get('SECRET')
    KEY = os.environ.get('KEY')

    f = Fernet(KEY.encode())

    
    connection = psycopg2.connect(
        user=BIDYOURAUCTION_USER,
        password=BIDYOURAUCTION_PASSWORD,
        host=BIDYOURAUCTION_HOST,
        port=BIDYOURAUCTION_PORT,
        database=BIDYOURAUCTION_DB
    )

    #[ [username, password, email], ... ]
    admins = [
        ["bruno", "faria", "brunofaria@email.com"],
        ["rita", "rodrigues", "ritarodrigues@email.com"],
        ["dylan", "perdigao", "dylanperdigao@email.com"]
    ]

    
    try:
        for i in range(len(admins)):
            enc = f.encrypt(admins[i][1].encode())
            
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO admin (person_username, person_email, person_password)
                VALUES (%s,%s,%s);
                """, (admins[i][0], admins[i][2], enc.decode()))

        connection.commit()

    except Exception as e:
        connection.rollback()
        print(e)
