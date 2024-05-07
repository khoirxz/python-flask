# app/models/auth.py

from flask_mysqldb import MySQL
from cryptography.fernet import Fernet
from config import Config

mysql = MySQL()

def signup_user(email, username, password):
    """Register new user"""
    with mysql.connection.cursor() as cur:

        # Enkripsi password
        encrypted_password = Fernet(Config.SECRET_KEY.encode('utf-8')).encrypt(password.encode('utf-8'))

        # check jika username sudah ada
        cur.execute("SELECT id FROM user WHERE username = %s", (username,))
        result = cur.fetchone()

        if result:
            return {'status': 'error', 'message': 'Username sudah ada'}

        cur.execute("INSERT INTO user (email, username, password) VALUES (%s, %s, %s)",
                   (email, username, encrypted_password))
        mysql.connection.commit()

    return {'status': 'success', 'message': 'Signup berhasil'}

def login_user(username, password):
    """Login user"""
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM user WHERE username = %s", (username,))
        user = cur.fetchone()

        decripted_password = Fernet(Config.SECRET_KEY.encode('utf-8')).decrypt(user['password']).decode('utf-8')
        print(Fernet(Config.SECRET_KEY.encode('utf-8')).encrypt(user['username'].encode('utf-8'))) 

        if user and decripted_password == password:
            return {'status': 'success', 'message': 'Login berhasil', 'user': Fernet(Config.SECRET_KEY.encode('utf-8')).encrypt(user['username'].encode('utf-8'))}
        else:
            return {'status': 'error', 'message': 'Email atau password salah'}

def verify_user(username):
    """Verify user by decrypting the username"""
    try:
        
        username = Fernet(Config.SECRET_KEY.encode('utf-8')).decrypt(username).decode('utf-8')
        return {'status': 'success', 'message': 'Username valid', 'username': username}
    except:
        return {'status': 'error', 'message': 'Username tidak valid'}
