import sqlite3
from sqlite3 import Error

def create_db_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Running sqlite3 version " + str(sqlite3.version))
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':

    #WINDOWS
    # create_db_connection("raids_sql.db")

    #UBUNTU
    create_db_connection("/home/ben/github/raids_bot/raids_sql.db")