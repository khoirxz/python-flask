from flask_mysqldb import MySQL

mysql = MySQL()


def get_all():
    """Get all penggunaan pakan"""
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM penggunaan_pakan ORDER BY tanggal DESC")
        result = cur.fetchall()
        if result is None:
            return {"status": "error", "message": "id not found"}
    return result


def get_by_id(id):
    """Get penggunaan pakan by id"""
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM penggunaan_pakan WHERE id=%s", (id,))
        result = cur.fetchone()
        if result is None:
            return {"status": "error", "message": "id not found"}
    return result


def insert(tanggal, jenis_pakan, nomor_kandang, pagi, sore, total):
    """Insert penggunaan pakan"""
    with mysql.connection.cursor() as cur:
        cur.execute(
            "INSERT INTO penggunaan_pakan (tanggal, jenisPakan, nomorKandang, pagi, sore, total) VALUES (%s, %s, %s, %s, %s, %s)",
            (tanggal, jenis_pakan, nomor_kandang, pagi, sore, total),
        )
        mysql.connection.commit()
    return {"status": "success", "message": "Input penggunaan pakan berhasil"}


def update(id, tanggal, jenis_pakan, nomor_kandang, pagi, sore, total):
    """Update penggunaan pakan"""
    with mysql.connection.cursor() as cur:
        cur.execute(
            "UPDATE penggunaan_pakan SET tanggal=%s, jenisPakan=%s, nomorKandang=%s, pagi=%s, sore=%s, total=%s WHERE id=%s",
            (tanggal, jenis_pakan, nomor_kandang, pagi, sore, total, id),
        )
        mysql.connection.commit()
    return {"status": "success", "message": "Update penggunaan pakan berhasil"}


def delete(id):
    """Delete penggunaan pakan"""
    with mysql.connection.cursor() as cur:
        cur.execute("DELETE FROM penggunaan_pakan WHERE id=%s", (id,))
        mysql.connection.commit()
    return {"status": "success", "message": "Delete penggunaan pakan berhasil"}