import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="#Follow3Blues",
        database="predictive_maintenance"
    )
