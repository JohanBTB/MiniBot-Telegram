import psycopg2

def closeConnection(conn):
    conn.close()
    conn.cursor.close()
    print("Se cerro la coneccion PostgreSQL")
    
def startConnection():
    try:
        conn = psycopg2.connect(
            host="hostname",
            database="databasename",
            user="username",
            password="password"
        )
        return conn
    except psycopg2.Error as e:
        print("Sucedio un error al tratar de conectarse a la base de datos.\ne")
    finally:
        if(conn):
            closeConnection(conn)


def testConnection(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("Select * from Users")
        conn.commit()
    except psycopg2.Error as e:
        print("No salio el test de coneccion\ne")
    finally:
        if (conn):
            closeConnection(conn)

