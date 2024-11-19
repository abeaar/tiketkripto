import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",  # Ganti dengan host MySQL Anda, biasanya localhost
            user="root",  # Ganti dengan username MySQL Anda
            password="",  # Ganti dengan password MySQL Anda, jika ada
            database="kripto",  # Ganti dengan nama database yang Anda pakai
            connection_timeout=60  # Set timeout untuk menghindari koneksi terputus
        )
        
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None
