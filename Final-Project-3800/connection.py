import mysql.connector

def get_db():
     return mysql.connector.connect(
        host="localhost",
        user="root",
        password="C@t23321",
        database="cd_database")