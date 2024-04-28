# app/models/stok_pakan.py

from flask_mysqldb import MySQL

mysql = MySQL()

def get_all():
    """Get all stok pakan"""
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM stok_pakan ORDER BY tanggal DESC")
        result = cur.fetchall()
        if result is None:
            return {'status': 'error', 'message': 'id not found'}
    return result

def get_by_id(id):
    """Get stok pakan by id"""
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM stok_pakan WHERE id=%s", (id,))
        result = cur.fetchone()
        if result is None:
            return {'status': 'error', 'message': 'id not found'}
    return result

def insert(tanggal, jenis_pakan, jumlah_masuk, jumlah_penggunaan, total_stok, kondisi):
    """Insert stok pakan"""
    with mysql.connection.cursor() as cur:
        cur.execute(
            "INSERT INTO stok_pakan (tanggal, jenisPakan, jumlahPakanMasuk, jumlahPenggunaanPakan, totalStokTersedia, kondisiStokPakan) VALUES (%s, %s, %s, %s, %s, %s)",
            (tanggal, jenis_pakan, jumlah_masuk, jumlah_penggunaan, total_stok, kondisi),
        )

        mysql.connection.commit()
    return {"status": "success", "message": "Input stok pakan berhasil"}

def update(id, tanggal, jenis_pakan, jumlah_masuk, jumlah_penggunaan, total_stok, kondisi):
    """Update stok pakan"""
    with mysql.connection.cursor() as cur:
        cur.execute(
            "UPDATE stok_pakan SET tanggal=%s, jenisPakan=%s, jumlahPakanMasuk=%s, jumlahPenggunaanPakan=%s, totalStokTersedia=%s, kondisiStokPakan=%s WHERE id=%s",
            (tanggal, jenis_pakan, jumlah_masuk, jumlah_penggunaan, total_stok, kondisi, id),
        )

        mysql.connection.commit()
    return {"status": "success", "message": "Update stok pakan berhasil"}

def delete(id):
    """Delete stok pakan"""
    with mysql.connection.cursor() as cur:
        cur.execute("DELETE FROM stok_pakan WHERE id=%s", (id,))

        mysql.connection.commit()
    return {"status": "success", "message": "Delete stok pakan berhasil"}