from getpass import getpass
from mysql.connector import connect, Error
import os

try:
    with connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
    ) as connection:
        print("CONECTOU NA DATABASE:", connection)
        cursor = connection.cursor().execute("SHOW DATABASES")
        for db in cursor:
            print(db)
except Error as e:
    print(e)
