from cryptography.fernet import Fernet

#key = Fernet.generate_key()
#to generate new key

key = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='

f = Fernet(key)

enc = f.encrypt(bytes("pass", "utf-8"))
dec = f.decrypt(enc)
print(dec.decode("utf-8"))

print("abc")
print("abc".encode())
print("abc".encode().decode())

