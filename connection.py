import psycopg2

def connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="MyBot",
            user="postgres",
            password="johan12.com"
        )
        return conn

    except psycopg2.Error as e:
        print(f"C.0 Sucedio un error al tratar de conectarse a la base de datos.\n{e}")

conn = connection()

# DECORATOR1 - Para el try y los mensajes de error
def error1(errorMessage):
    def decorator(func):
        def wrapper(*args, **kwargs):
            
            try:
                conn = connection()
                kwargs['conn'] = conn
                result = func(*args,**kwargs)
                close_connection(conn)
            except psycopg2.Error as e:
                print(f"{errorMessage}\n{e}")

            return result
        return wrapper
    return decorator

# DECORATOR1 - Para el try y los mensajes de error
def error2(errorMessage):
    def decorator(func):
        def wrapper(*args, **kwargs):
            global conn
            try:
                func(*args,**kwargs)

            except psycopg2.Error as e:
                print(f"{errorMessage}\n{e}")
                conn.rollback()
                conn.close()
        return wrapper
    return decorator


def close_connection(conn):
    try:
        conn.cursor().close()
        conn.close()
        print("Se cerro la coneccion PostgreSQL")
    except psycopg2.Error as e:
        print(F"C.1 No se pudo cerrar correctamente la coneccion.\n{e}")



def test_connection():
    try:
        conn = connection()
        cursor = conn.cursor()
        print("#####")
        print(cursor.execute("Select * from Chats"))
        
        conn.commit()
        users = cursor.fetchall()

        for user in users:
            print(user)
    except psycopg2.Error as e:
        print(f"Se salio el test de coneccion\n{e}")
    finally:
        if(conn):
            close_connection(conn)

@error1 (errorMessage = "C.2 Fallo la coneccion al verificar usuario.")
def verify_user(CHAT_ID, conn = None):
        cursor = conn.cursor()
        exist = True
        cursor.execute("Select * from chats where id = %s", (CHAT_ID,))
        chat = cursor.fetchone()
        if not chat:
            cursor.execute("Insert into chats values(%s)", (CHAT_ID,))
            conn.commit()
            print("Es nuevo")
            exist = False
        return exist, chat

@error2 (errorMessage="C.3 Fallo algo al crear el usuario.")
def creating_user(CHAT_ID, userName, userNickname):
    global conn
    conn = connection()

    cursor = conn.cursor()
    cursor.execute("INSERT INTO users(chat_id,name,nickname) VALUES(%s,%s,%s)",(CHAT_ID,userName,userNickname))
    # conn.commit()
    return True
    
@error1 (errorMessage="C.4 Fallo al conseguir el informacion del usuario.")
def get_user_info(CHAT_ID, column, conn = None):
    cursor = conn.cursor()
    cursor.execute("SELECT {} FROM users where chat_id = %s".format(column), (CHAT_ID,))
    usuario = cursor.fetchone()
    
    return usuario[0]

@error2 (errorMessage="C.5 Fallo al actualizar o guardar informacion.")
def update_info(CHAT_ID, column,value, cerrar=True):
    global conn
    if conn.closed != 0:
        conn = connection()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE users SET {} = %s WHERE chat_id = %s".format(column), (value,CHAT_ID))
    conn.commit()
    if cerrar:
        close_connection(conn)
    