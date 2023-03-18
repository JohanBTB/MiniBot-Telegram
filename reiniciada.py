import psycopg2
try:

    conn = psycopg2.connect(
        host="localhost",
        database="MyBot",
        user="postgres",
        password=""
    )
    print("a")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE users")
    cursor.execute("DROP TABLE chats")

    cursor.execute(
    """CREATE TABLE Chats(
	    id int PRIMARY KEY,
	    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    
    );""")

    cursor.execute("""CREATE TABLE Users(
	id INT GENERATED ALWAYS AS IDENTITY,
	chat_id INT NOT NULL,
	name VARCHAR(30) NOT NULL,
	nickname VARCHAR(30) NULL,
	email VARCHAR(30) NULL,
	CONSTRAINT fk_chat
	FOREIGN KEY(chat_id)
	REFERENCES chats(id)
	ON DELETE CASCADE
    );""")

    cursor.execute("""CREATE TABLE Products(
	id INT GENERATED ALWAYS AS IDENTITY,
	chat_id INT NOT NULL,
	name VARCHAR(30),
	unit INT, 
	dued_at TIMESTAMP, 
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
	CONSTRAINT fk_chat
	FOREIGN KEY(chat_id)
	REFERENCES chats(id)
	ON DELETE CASCADE
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Se reiniciaron las tablas")

except psycopg2.Error as e:
    print(f"C.0 Sucedio un error al tratar de conectarse a la base de datos.\n{e}")