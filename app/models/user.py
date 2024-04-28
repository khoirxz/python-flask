# app/model/user.py

from flask_mysqldb import MySQL
from cryptography.fernet import Fernet

mysql = MySQL()

def get_all():
    """Get all user"""
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM user")
        result = cur.fetchall()
        if result is None:
            return {'status': 'error', 'message': 'id not found'}
    return result

def get_by_id(id):
    """Get user by id"""
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM user WHERE id=%s", (id,))
        result = cur.fetchone()
        if result is None:
            return {'status': 'error', 'message': 'id not found'}
    return result

def update(id, username, email, password):
    """Update user"""
    with mysql.connection.cursor() as cur:
        
        token = 'Dsw0UkKz2eNsFVPlo2u12F5EsfnhONa9pOhZbbBGTdM='
        encrypted_password = Fernet(token.encode('utf-8')).encrypt(password.encode('utf-8'))

        cur.execute("UPDATE user SET username=%s, email=%s, password=%s WHERE id=%s", (username, email, encrypted_password, id))
        mysql.connection.commit()
    return {'status': 'success', 'message': 'Update user berhasil'}

def delete(id):
    """Delete user"""
    with mysql.connection.cursor() as cur:
        cur.execute("DELETE FROM user WHERE id=%s", (id,))
        mysql.connection.commit()
    return {'status': 'success', 'message': 'Delete user berhasil'}