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
        print("Se inicio la coneccion PostgreSQL")
    except psycopg2.Error as e:
        print(f"C.0 Sucedio un error al trat|ar de conectarse a la base de datos.\n{e}")

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

# VERIFYING
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

@error1 (errorMessage = "C.2.1 Fallo la coneccion al verificar el producto.")
def verify_product(nombre, conn = None):
    cursor = conn.cursor()
    exist = True
    cursor.execute("Select id, name, unit, dued_at from products where name = LOWER(%s)",(nombre,) )
    product = cursor.fetchone()
    
    if product is None:
        product = {'name':nombre,'unit':0,'dued_at':''}
        print("Es nuevo producto")
        exist = False
        return exist, product
    product = {'id':product[0],'name':product[1],'unit':product[2],'dued_at':product[3]}
    return exist, product
# ---------------------------------------------------------------------------------------------------
# CREATING
@error2 (errorMessage="C.3 Fallo algo al crear el usuario.")
def creating_user(CHAT_ID, userName, userNickname):
    global conn
    conn = connection()

    cursor = conn.cursor()
    cursor.execute("INSERT INTO users(chat_id,name,nickname) VALUES(%s,%s,%s)",(CHAT_ID,userName,userNickname))
    conn.commit()
    return True

@error2 (errorMessage = "C.3.1 Fallo algo al crear el producto.")
def creating_product(CHAT_ID, product):
    global conn
    conn = connection()

    cursor = conn.cursor()
    cursor.execute("INSERT INTO products(chat_id,name,unit,dued_at) VALUES(%s,%s,%s,%s)",(CHAT_ID,product['name'], product['unit'],product['dued_at']))
    conn.commit()
    close_connection(conn)
    return True
# ---------------------------------------------------------------------------------------------------
# GETTING DATA
@error1 (errorMessage="C.4 Fallo al conseguir el informacion del usuario.")
def get_user_info(CHAT_ID, column, conn = None):
    cursor = conn.cursor()
    cursor.execute("SELECT {} FROM users where chat_id = %s".format(column), (CHAT_ID,))
    usuario = cursor.fetchone()
    
    return usuario[0]
@error1 (errorMessage="C.4.1 Fallo al conseguir informacion de la tabla productos")
def get_product(CHAT_ID, id_product, conn = None):
    cursor = conn.cursor()
    cursor.execute("SELECT id,name, unit, dued_at FROM products where chat_id = %s and id = %s", (CHAT_ID, id_product))
    producto = cursor.fetchone()
    producto = {'id':producto[0],'name':producto[1],'unit':producto[2],'dued_at':producto[3]}
    return producto

@error1 (errorMessage="C.4.1 Fallo al conseguir el informacion de la tabla productos.")
def get_products(CHAT_ID, value, conn = None):
    cursor = conn.cursor()
    cursor.execute("SELECT id,name FROM products where name like '%{}%'".format(value))
    rows = cursor.fetchmany()
    result = []
    while rows:
        result.extend(rows)
        rows = cursor.fetchmany()
    return result
# ---------------------------------------------------------------------------------------------------
# UPDATING
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

@error2 (errorMessage="C.5.1 Fallo al actualizar o guardar el producto.")
def update_product(CHAT_ID,product, cerrar=True ):
    global conn
    if conn.closed != 0:
        conn = connection()
    cursor = conn.cursor()
    keys = list(product.keys())
    id_product = product['id']
    for i in range (2,4):
        key = keys[i]

        cursor.execute("UPDATE products SET {} = %s WHERE chat_id = %s AND id = %s".format(key), (product[key],CHAT_ID, id_product))
    cursor.execute("UPDATE products SET updated_at = CURRENT_TIMESTAMP WHERE chat_id = %s AND id = %s", (CHAT_ID, id_product))
    conn.commit()
    if cerrar:
        close_connection(conn)
# ---------------------------------------------------------------------------------------------------
# DELETING
@error1 (errorMessage = "C.2.1 Fallo la la eliminacion de un producto.")
def delete_product(CHAT_ID,id_product, conn = None):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products where chat_id = %s and id = %s", (CHAT_ID, int(id_product)))
    conn.commit()
    return True
    