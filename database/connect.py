import mysql.connector
from mysql.connector import Error

def creat_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'E-Commerce-app'
        )

        if connection.is_connected():
            print("Connected to the Database successfully")
    except Error as e:
        print(f"Error: '{e}' occurred")

    return connection

# creat_connection()