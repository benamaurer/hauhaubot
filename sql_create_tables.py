import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    #WINDOWS
    # database = "raids_sql.db"

    #UBUNTU
    database = "/home/ben/github/raids_bot/raids_sql.db"


    sql_create_timers_table = """CREATE TABLE IF NOT EXISTS timers (id integer PRIMARY KEY, discord_id integer, reminder_type text, reminder_item text, request_time text, end_time text, sent integer); """

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_timers_table)
    else:
        print("Error: Unable to create timers sql table!")

if __name__ == '__main__':
    main()