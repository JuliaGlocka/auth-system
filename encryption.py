import os
import bcrypt
from cryptography.fernet import Fernet, InvalidToken
from config import key_file

if not os.path.exists(key_file):
    with open(key_file, 'wb') as keyfile:
        key = Fernet.generate_key()
        keyfile.write(key)
else:
    with open(key_file, 'rb') as keyfile:
        key = keyfile.read()

cipher = Fernet(key)

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def encrypt_data(data):
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(data):
    try:
        return cipher.decrypt(data.encode()).decode()
    except InvalidToken:
        print("Decryption error: Data may be corrupted or invalid.")
        return None
