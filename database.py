import sqlite3

def conectar():
    conn = sqlite3.connect("produtos.db")
    return conn

def criar_tabela():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria TEXT,
        quantidade INTEGER,
        validade TEXT
    )
    """)

    conn.commit()
    conn.close()


def adicionar_produto(nome, categoria, quantidade, validade):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO produtos (nome, categoria, quantidade, validade)
    VALUES (?, ?, ?, ?)
    """, (nome, categoria, quantidade, validade))

    conn.commit()
    conn.close()


def listar_produtos():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produtos")

    dados = cursor.fetchall()

    conn.close()

    return dados