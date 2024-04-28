# app/models/riwayat.py

from flask_mysqldb import MySQL

mysql = MySQL()

def get_all():
    """Get all riwayat"""
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM riwayat ORDER BY tanggal DESC")
        result = cur.fetchall()
        if result is None:
            return {'status': 'error', 'message': 'id not found'}
    return result

def get_by_id(id):
    """Get riwayat by id"""
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM riwayat WHERE id=%s", (id,))
        result = cur.fetchone()
        if result is None:
            return {'status': 'error', 'message': 'id not found'}
    return result

def insert(tanggal, model_regresi, hari_mulai_prediksi, jumlah_prediksi):
    """Insert riwayat"""
    with mysql.connection.cursor() as cur:
        cur.execute("INSERT INTO riwayat (tanggal, modelRegresi, hariMulaiPrediksi, jumlahHariDiprediksi) VALUES (%s, %s, %s, %s)", 
                    (tanggal, model_regresi, hari_mulai_prediksi, jumlah_prediksi))
        mysql.connection.commit()
    return {'status': 'success', 'message': 'Input riwayat berhasil'}

def update(id, tanggal, model_regresi, hari_mulai_prediksi, jumlah_prediksi):
    """Update riwayat"""
    with mysql.connection.cursor() as cur:
        cur.execute("UPDATE riwayat SET tanggal=%s, modelRegresi=%s, hariMulaiPrediksi=%s, jumlahHariDiprediksi=%s WHERE id=%s", 
                    (tanggal, model_regresi, hari_mulai_prediksi, jumlah_prediksi, id))
        mysql.connection.commit()
    return {'status': 'success', 'message': 'Update riwayat berhasil'}

def delete(id):
    """Delete riwayat"""
    with mysql.connection.cursor() as cur:
        cur.execute("DELETE FROM riwayat WHERE id=%s", (id,))
        mysql.connection.commit()
    return {'status': 'success', 'message': 'Delete riwayat berhasil'}