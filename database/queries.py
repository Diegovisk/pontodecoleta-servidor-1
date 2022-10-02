from getpass import getpass
from mysql.connector import connect, Error
import os

def create_table():
    create_caixas_table_query = """
    CREATE TABLE Caixas(
        id_caixa INT AUTO_INCREMENT PRIMARY KEY,
        nome_caixa VARCHAR(100)
    )
    """

    create_doacao_table_query = """
    CREATE TABLE Doacoes(
        id_objeto INT AUTO_INCREMENT PRIMARY KEY,
        classe_doacao VARCHAR(50),
        horario_docacao INT,
        id_caixa_fk INT,
        FOREIGN KEY (id_caixa_fk) REFERENCES Caixas(id_caixa)
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
                connection.commit()
                print("SUCESSO EM CRIAR TABELAS")
    except Error as e:
        print(e)

def insert_data_caixas():
    insert_data_values = """
    INSERT INTO Caixas (nome_caixa)
    VALUES
        ("EST"),
        ("ENS"),
        ("ESAT"),
        ("ESO"),
        ("Manauara"),
        ("Amazonas"),
        ("Sumauma")
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
                cursor.execute(insert_data_values)
                connection.commit()
                print("SUCESSO EM INSERIR VALORES DA CAIXA")
    except Error as e:
        print(e)

def insert_data_doacoes():
    insert_data_values = """
    INSERT INTO Doacoes (classe_doacao, horario_docacao, id_caixa_fk)
    VALUES
        ("feijao",1664673048,1),
        ("feijao",1664673152,1),
        ("arroz",1664673163,2),
        ("feijao",1664673163,3),
        ("feijao",1664673183,1),
        ("feijao",1664673192,2),
        ("macarrao",1664673203,1)
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
                cursor.execute(insert_data_values)
                connection.commit()
                print("SUCESSO EM INSERIR VALORES DO ALIMENTO")
    except Error as e:
        print(e)


## SETUP 
create_table()
insert_data_caixas()
insert_data_doacoes()