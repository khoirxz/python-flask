from flask_mysqldb import MySQL

mysql = MySQL()

def check_db():
    status = True
    version = None
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT VERSION()")
        version = cur.fetchone()
    except:
        status = False
    return status, version

