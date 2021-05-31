# imports
import psycopg2
from cryptography.fernet import Fernet

if __name__ == '__main__':

    BIDYOURAUCTION_HOST = "ec2-34-254-69-72.eu-west-1.compute.amazonaws.com"
    BIDYOURAUCTION_PORT = "5432"
    BIDYOURAUCTION_DB = "das7ket3c5aarn"
    BIDYOURAUCTION_PASSWORD = "eb4ada6829ffce0e0f516062ea258ca6aa14d2fd85ea907ad910aa62eaf1412a"
    BIDYOURAUCTION_USER = "vtxuzrplfviiht"
    
    #Fernet.generate_key()
    #to generate new key
    KEY = 'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='

    f = Fernet(bytes(KEY, "utf-8"))

    
    connection = psycopg2.connect(
        user=BIDYOURAUCTION_USER,
        password=BIDYOURAUCTION_PASSWORD,
        host=BIDYOURAUCTION_HOST,
        port=BIDYOURAUCTION_PORT,
        database=BIDYOURAUCTION_DB
    )

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
