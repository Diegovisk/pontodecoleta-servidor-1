from getpass import getpass
from mysql.connector import connect, Error
import os

def create_table():
    create_caixas_table_query = """
    CREATE TABLE Caixas(
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100)
    )
    """

    create_doacao_table_query = """
    CREATE TABLE Doacoes(
        id INT AUTO_INCREMENT PRIMARY KEY,
        doacao VARCHAR(50),
        timestamp UNSIGNED BIG INT,
        id_caixa INT,
        FOREIGN KEY (id_caixa) REFERENCES Caixas(id)
    )
    """

    create_capacity_table_query = """
    CREATE TABLE Capacidades(
        id INT AUTO_INCREMENT PRIMARY KEY,
        cm_restantes FLOAT,
        id_caixa INT,
        timestamp UNSIGNED BIG INT,
        FOREIGN KEY (id_caixa) REFERENCES Caixas(id)
    )
    """

    create_collects_table_query = """
    CREATE TABLE Coletas(
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp UNSIGNED BIG INT,
        id_caixa INT,
        FOREIGN KEY (id_caixa) REFERENCES Caixas(id)
    )
    """

    try:
        with connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        ) as connection:
            print("CONECTADO")
            with connection.cursor() as cursor:
                cursor.execute(create_caixas_table_query)
                cursor.execute(create_doacao_table_query)
                cursor.execute(create_capacity_table_query)
                cursor.execute(create_collects_table_query)
                connection.commit()
                print("SUCESSO EM CRIAR TABELAS")
    except Error as e:
        print(e)

# Create row in Caixas table 
def create_caixa(nome_caixa):
    create_caixa_query = """
    INSERT INTO Caixas (nome_caixa)
    VALUES (%s)
    """
    try:
        with connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        ) as connection:
            print("CONECTADO")
            with connection.cursor() as cursor:
                cursor.execute(create_caixa_query, (nome_caixa,))
                connection.commit()
                print("SUCESSO EM INSERIR VALORES DA CAIXA")
    except Error as e:
        print(e)

# Insert row in Capacidades table with timestamp
def insert_capacidade(cm_restantes, id_caixa):
    create_capacidade_query = """
    INSERT INTO Capacidades (cm_restantes, id_caixa, timestamp)
    VALUES (%s, %s, UNIX_TIMESTAMP())
    """
    try:
        with connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        ) as connection:
            print("CONECTADO")
            with connection.cursor() as cursor:
                cursor.execute(create_capacidade_query, (cm_restantes, id_caixa))
                connection.commit()
                print("SUCESSO EM INSERIR VALORES DA CAPACIDADE")
    except Error as e:
        print(e)

# Insert row in Doacoes table
def insert_doacao(doacao, id_caixa):
    create_doacao_query = """
    INSERT INTO Doacoes (doacao, id_caixa, timestamp)
    VALUES (%s, %s, UNIX_TIMESTAMP())
    """
    try:
        with connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        ) as connection:
            print("CONECTADO")
            with connection.cursor() as cursor:
                cursor.execute(create_doacao_query, (doacao, id_caixa))
                connection.commit()
                print("SUCESSO EM INSERIR VALORES DA DOAÇÃO")
    except Error as e:
        print(e)

# Do a coleta
def coleta(id_caixa):
    create_coleta_query = """
    INSERT INTO Coletas (id_caixa, timestamp)
    VALUES (%s, UNIX_TIMESTAMP())
    """
    try:
        with connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        ) as connection:
            print("CONECTADO")
            with connection.cursor() as cursor:
                cursor.execute(create_coleta_query, (id_caixa,))
                connection.commit()
                print("SUCESSO EM INSERIR VALORES DA COLETA")
    except Error as e:
        print(e) 

## SETUP 
create_table()