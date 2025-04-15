import mysql.connector # type: ignore
from mysql.connector import Error # type: ignore

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            user='root',
            password='',
            host='localhost',
            database='fairshare'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None