import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="perez",
        password="perez123",
        database="techgear_db"
    )