# from getpass import getpass
from random import randint, uniform
from secrets import choice
from time import time
from mysql.connector import connect, Error
import os
from dotenv import load_dotenv

load_dotenv()

def create_tables():
    create_caixas_table_query = """
    CREATE TABLE IF NOT EXISTS Caixas(
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100)
    )
    """

    create_doacao_table_query = """
    CREATE TABLE IF NOT EXISTS Doacoes(
        id INT AUTO_INCREMENT PRIMARY KEY,
        doacao VARCHAR(50) NOT NULL,
        timestamp BIGINT UNSIGNED NOT NULL,
        id_caixa INT NOT NULL,
        FOREIGN KEY (id_caixa) REFERENCES Caixas(id)
    )
    """

    create_capacity_table_query = """
    CREATE TABLE IF NOT EXISTS Capacidades(
        id INT AUTO_INCREMENT PRIMARY KEY,
        cm_restantes FLOAT NOT NULL,
        id_caixa INT NOT NULL,
        timestamp BIGINT UNSIGNED NOT NULL,
        FOREIGN KEY (id_caixa) REFERENCES Caixas(id)
    )
    """

    create_collects_table_query = """
    CREATE TABLE IF NOT EXISTS Coletas(
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp BIGINT UNSIGNED NOT NULL,
        id_caixa INT NOT NULL,
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
    INSERT INTO Caixas (nome)
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
                return cursor.lastrowid
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


# Setup dummy data
def setup_dummy_data():
    # Create one box
    now = time()
    now = int(now)

    dummy_coletas_n = randint(1, 3)
    donation_choices = ["FEIJAO", "ARROZ", "MACARRAO"]
    
    id_caixa = create_caixa("Caixa Padrão " + str(now))

    for _ in range(dummy_coletas_n):
        capacity = 100
        dummy_donation_n = randint(20,30)
        print("Criando {} doações".format(dummy_donation_n))
        for __ in range(dummy_donation_n):
            # add 10 minutes to timestamp
            now += 600
            create_doacao_query = """
            INSERT INTO Doacoes (doacao, id_caixa, timestamp)
            VALUES (%s, %s, %s)
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
                        cursor.execute(create_doacao_query, (choice(donation_choices), id_caixa, now))
                        connection.commit()
                        print("INSERIDO {}, NA CAIXA {}, NO MOMENTO {}".format(choice(donation_choices), id_caixa, now))
            except Error as e:
                print(e)

            # Submit a capacity
            capacity -= uniform(50/dummy_donation_n, 100/dummy_donation_n)
            create_capacidade_query = """
            INSERT INTO Capacidades (cm_restantes, id_caixa, timestamp)
            VALUES (%s, %s, %s)
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
                        cursor.execute(create_capacidade_query, (capacity, id_caixa, now))
                        connection.commit()
                        print("INSERIDO {}cm, NA CAIXA {}, NO MOMENTO {}".format(capacity, id_caixa, now))
            except Error as e:
                print(e)
        now += randint(1, 100)
        create_coleta_query = """
        INSERT INTO Coletas (id_caixa, timestamp)
        VALUES (%s, %s)
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
                    cursor.execute(create_coleta_query, (id_caixa, now))
                    connection.commit()
                    print("INSERIDO COLETA, NA CAIXA {}, NO MOMENTO {}".format(id_caixa, now))
        except Error as e:
            print(e)

        
