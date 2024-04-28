# app/models/penerimaan_pakan.py

from flask_mysqldb import MySQL

mysql = MySQL()

def get_all():
    """Get all penerimaan pakan"""
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM penerimaan_pakan ORDER BY tanggal DESC")
        result = cur.fetchall()
        if result is None:
            return {'status': 'error', 'message': 'id not found'}
    return result

def get_by_id(id):
    """Get penerimaan pakan by id"""
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM penerimaan_pakan WHERE id=%s", (id,))
        result = cur.fetchone()
        if result is None:
            return {'status': 'error', 'message': 'id not found'}
    return result

def insert(tanggal, kode_pakan, jenis, jumlah_pakan, kondisi, sumber):
    """Insert penerimaan pakan"""
    with mysql.connection.cursor() as cur:
        cur.execute("INSERT INTO penerimaan_pakan (tanggal, kodePakan, jenisPakan, jumlahPakan, kondisiPakan, SumberStokPakan) VALUES (%s, %s, %s, %s, %s, %s)",
                    (tanggal, kode_pakan, jenis, jumlah_pakan, kondisi, sumber))
        mysql.connection.commit()
    return {'status': 'success', 'message': 'Input penerimaan pakan berhasil'}

def update(id, tanggal, kode_pakan, jenis, jumlah_pakan, kondisi, sumber):
    """Update penerimaan pakan"""
    with mysql.connection.cursor() as cur:
        cur.execute("UPDATE penerimaan_pakan SET tanggal=%s, kodePakan=%s, jenisPakan=%s, jumlahPakan=%s, kondisiPakan=%s, SumberStokPakan=%s WHERE id=%s",
                    (tanggal, kode_pakan, jenis, jumlah_pakan, kondisi, sumber, id))
        mysql.connection.commit()
    return {'status': 'success', 'message': 'Update penerimaan pakan berhasil'}

def delete(id):
    """Delete penerimaan pakan"""
    with mysql.connection.cursor() as cur:
        cur.execute("DELETE FROM penerimaan_pakan WHERE id=%s", (id,))
        mysql.connection.commit()
    return {'status': 'success', 'message': 'Delete penerimaan pakan berhasil'}