# app/model/pembelian_pakan.py

from flask_mysqldb import MySQL

mysql = MySQL()

def get_all():
    """Get all pembelian pakan"""
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM pembelian_pakan ORDER BY tanggal DESC")
        result = cur.fetchall()
        if result is None:
            return {"status": "error", "message": "id not found"}
    return result

def get_by_id(id):
    """Get pembelian pakan by id"""
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM pembelian_pakan WHERE id=%s", (id,))
        result = cur.fetchone()
        if result is None:
            return {"status": "error", "message": "id not found"}
    return result

def insert(tanggal, nama_pakan, supplier, item, jumlah_pakan):
    """Insert pembelian pakan"""
    with mysql.connection.cursor() as cur:
        cur.execute(
            "INSERT INTO pembelian_pakan (tanggal, namaPakan, supplier, item, jumlahPakan) VALUES (%s, %s, %s, %s, %s)",
            (tanggal, nama_pakan, supplier, item, jumlah_pakan),
        )
        mysql.connection.commit()
    return {"status": "success", "message": "Input pembelian pakan berhasil"}

def update(id, tanggal, nama_pakan, supplier, item, jumlah_pakan):
    """Update pembelian pakan"""
    with mysql.connection.cursor() as cur:
        cur.execute(
            "UPDATE pembelian_pakan SET tanggal=%s, namaPakan=%s, supplier=%s, item=%s, jumlahPakan=%s WHERE id=%s",
            (tanggal, nama_pakan, supplier, item, jumlah_pakan, id),
        )
        mysql.connection.commit()
    return {"status": "success", "message": "Update pembelian pakan berhasil"}


def delete(id):
    """Delete pembelian pakan"""
    with mysql.connection.cursor() as cur:
        cur.execute("DELETE FROM pembelian_pakan WHERE id=%s", (id,))
        mysql.connection.commit()
    return {"status": "success", "message": "Delete pembelian pakan berhasil"}