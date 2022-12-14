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
            database=os.getenv("MYSQL_DATABASE"),
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
            database=os.getenv("MYSQL_DATABASE"),
        ) as connection:
            print("CONECTADO")
            with connection.cursor() as cursor:
                cursor.execute(create_caixa_query, (nome_caixa,))
                connection.commit()
                print("SUCESSO EM INSERIR VALORES DA CAIXA")
                return cursor.lastrowid
    except Error as e:
        print(e)


# get all rows from Caixas table
def get_caixas():
    get_caixas_query = """
    SELECT * FROM Caixas
    """
    try:
        with connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
        ) as connection:
            print("CONECTADO")
            with connection.cursor() as cursor:
                cursor.execute(get_caixas_query)
                caixas = cursor.fetchall()
                print("SUCESSO EM BUSCAR CAIXAS")
                # to dict
                caixas = [
                    dict(zip([key[0] for key in cursor.description], caixa))
                    for caixa in caixas
                ]
                return caixas
    except Error as e:
        print(e)


# get rows from coletas table, ordered by timestamp, for a given id_caixa
def get_coletas(id_caixa):
    get_coletas_query = """
    SELECT * FROM Coletas
    WHERE id_caixa = %s
    ORDER BY timestamp ASC
    """
    try:
        with connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
        ) as connection:
            print("CONECTADO")
            with connection.cursor() as cursor:
                cursor.execute(get_coletas_query, (id_caixa,))
                coletas = cursor.fetchall()
                # to dict
                coletas = [
                    dict(zip([key[0] for key in cursor.description], coleta))
                    for coleta in coletas
                ]
                print("SUCESSO EM BUSCAR COLETAS")
                return coletas
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
            database=os.getenv("MYSQL_DATABASE"),
        ) as connection:
            print("CONECTADO")
            with connection.cursor() as cursor:
                cursor.execute(create_capacidade_query, (cm_restantes, id_caixa))
                connection.commit()
                print("SUCESSO EM INSERIR VALORES DA CAPACIDADE")
    except Error as e:
        print(e)


# get all rows from Capacidades table, ordered by timestamp, for a given id_caixa, between two timestamps
def get_capacidades(id_caixa, timestamp_inicial, timestamp_final):
    get_capacidades_query = """
    SELECT * FROM Capacidades
    WHERE id_caixa = %s AND timestamp BETWEEN %s AND %s
    ORDER BY timestamp ASC
    """
    try:
        with connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
        ) as connection:
            print("CONECTADO")
            with connection.cursor() as cursor:
                cursor.execute(
                    get_capacidades_query,
                    (id_caixa, timestamp_inicial, timestamp_final),
                )
                capacidades = cursor.fetchall()
                print("SUCESSO EM BUSCAR CAPACIDADES")
                # to dict
                capacidades = [
                    dict(zip([key[0] for key in cursor.description], capacidade))
                    for capacidade in capacidades
                ]
                return capacidades
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
            database=os.getenv("MYSQL_DATABASE"),
        ) as connection:
            print("CONECTADO")
            with connection.cursor() as cursor:
                cursor.execute(create_doacao_query, (doacao, id_caixa))
                connection.commit()
                print("SUCESSO EM INSERIR VALORES DA DOA????O")
    except Error as e:
        print(e)


# get rows from doacoes table, ordered by timestamp, for a given id_caixa, between two timestamps
def get_doacoes(id_caixa, timestamp_inicial, timestamp_final):
    get_doacoes_query = """
    SELECT * FROM Doacoes
    WHERE id_caixa = %s AND timestamp BETWEEN %s AND %s
    ORDER BY timestamp DESC
    """
    try:
        with connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
        ) as connection:
            print("CONECTADO")
            with connection.cursor() as cursor:
                cursor.execute(
                    get_doacoes_query, (id_caixa, timestamp_inicial, timestamp_final)
                )
                doacoes = cursor.fetchall()
                # to dict
                doacoes = [
                    dict(zip([key[0] for key in cursor.description], doacao))
                    for doacao in doacoes
                ]
                print("SUCESSO EM BUSCAR DOACOES")
                return doacoes
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
            database=os.getenv("MYSQL_DATABASE"),
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

    id_caixa = create_caixa("Caixa Padr??o " + str(now))

    for _ in range(dummy_coletas_n):
        capacity = 100
        dummy_donation_n = randint(20, 30)
        print("Criando {} doa????es".format(dummy_donation_n))
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
                    database=os.getenv("MYSQL_DATABASE"),
                ) as connection:
                    print("CONECTADO")
                    with connection.cursor() as cursor:
                        cursor.execute(
                            create_doacao_query,
                            (choice(donation_choices), id_caixa, now),
                        )
                        connection.commit()
                        print(
                            "INSERIDO {}, NA CAIXA {}, NO MOMENTO {}".format(
                                choice(donation_choices), id_caixa, now
                            )
                        )
            except Error as e:
                print(e)

            # Submit a capacity
            capacity -= uniform(50 / dummy_donation_n, 100 / dummy_donation_n)
            create_capacidade_query = """
            INSERT INTO Capacidades (cm_restantes, id_caixa, timestamp)
            VALUES (%s, %s, %s)
            """
            try:
                with connect(
                    host=os.getenv("MYSQL_HOST"),
                    user=os.getenv("MYSQL_USER"),
                    password=os.getenv("MYSQL_PASSWORD"),
                    database=os.getenv("MYSQL_DATABASE"),
                ) as connection:
                    print("CONECTADO")
                    with connection.cursor() as cursor:
                        cursor.execute(
                            create_capacidade_query, (capacity, id_caixa, now)
                        )
                        connection.commit()
                        print(
                            "INSERIDO {}cm, NA CAIXA {}, NO MOMENTO {}".format(
                                capacity, id_caixa, now
                            )
                        )
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
                database=os.getenv("MYSQL_DATABASE"),
            ) as connection:
                print("CONECTADO")
                with connection.cursor() as cursor:
                    cursor.execute(create_coleta_query, (id_caixa, now))
                    connection.commit()
                    print(
                        "INSERIDO COLETA, NA CAIXA {}, NO MOMENTO {}".format(
                            id_caixa, now
                        )
                    )
        except Error as e:
            print(e)
