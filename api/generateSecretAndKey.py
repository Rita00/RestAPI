# imports
from cryptography.fernet import Fernet
import os

if __name__ == '__main__':
    print("KEY:")
    print(Fernet.generate_key().decode())
    print("TOKEN:")
    print(str(os.urandom(24)).split("'")[1])
