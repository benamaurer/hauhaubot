import discord
from datetime import datetime, timedelta
from python_vlookup import python_vlookup as vlookup
import time
import sqlite3
from sqlite3 import Error
import csv
from dotenv import load_dotenv
import os


# Loading .env
load_dotenv()


token = str(os.getenv('token'))



def sql_connect(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def sql_create_timer(conn, timer):
    sql = """INSERT INTO timers(discord_id, reminder_type, reminder_item, request_time, end_time, sent) VALUES(?,?,?,?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, timer)
    conn.commit()

    return cur.lastrowid


def timer_list():
    timer_list


def timer_parse(message, author):

    parsed_message = message.replace("_timer ","")
    reminder_item = parsed_message
    now = datetime.now()

    if reminder_item == 'help':
        return 'All possible timers: ' + timer_list()

    # test_mins = 1
    item_mins = vlookup.vlookup(str(reminder_item),"plant_times.csv",3)
    then = now + timedelta(minutes = int(item_mins))
    # test_then = now + timedelta(minutes = int(test_mins))

    #WINDOWS
    database = "raids_sql.db"

    #LINUX
    # database = "/home/ben/github/raids_bot/raids_sql.db"

    try:
        reminder_type = vlookup.vlookup(str(reminder_item),"plant_times.csv",2)
    except:
        reminder_type = "none"
        print("Error: Unable to determine timer type, defaulting to untyped timer!")
        return "Error: Unable to determine timer type, defaulting to untyped timer!"


    conn = sql_connect(database)

    with conn:
        #reminder_id, discord_id, reminder_type, reminder_item, now, then, sent
        test_timer = (author, reminder_type, reminder_item, now, then, 0)
        print(str(author) + ", " + reminder_type + ", " + reminder_item + ", " + str(now) + ", " + str(then) + ", " + "0")
        sql_create_timer(conn, test_timer)
        if str(now.date()) == str(then.date()):
            then = then.strftime("at %I:%M %p")
        else:
            then = then.strftime("on %A at %I:%M %p")

    return "<@" + str(author) + "> Your timer was created, you will be reminded " + str(then) + "."


def get_timers():
    conn = sql_connect("raids_sql.db")
    cur = conn.cursor()
    sent = 0
    cur.execute("SELECT * FROM timers WHERE sent=?", (sent,))

    unsent_rows = cur.fetchall()

    try:
        print("Unsent timers: \n----------------------------")

        for row in unsent_rows:
            print(row)

        print("----------------------------\n")
        return unsent_rows
    except:
        print ("Error: Unable to fetch unsent rows!")
        return "no rows"


def ping_create(reminder_id, discord_id, reminder_type, reminder_item):

    if reminder_type=="tree" or reminder_type=="herb" or reminder_type=="birdhouse":
        return "<@" + str(discord_id) + ">, your " + str(reminder_item) + " " + str(reminder_type) + "s are ready. (id - " + str(reminder_id) + ")"
    else:
        return "<@" + str(discord_id) + "> your " + str(reminder_type) + " timer has finished."


def compare_time(reminder_time):

    now = datetime.now()

    def time_parse(time_in):
        parsed_time = str(time_in).replace(" ",", ").replace("-",", ").replace(":",", ").replace(".",", ")
        output = datetime.strptime(parsed_time, '%Y, %m, %d, %H, %M, %S, %f')
        return output

    if (time_parse(now) > time_parse(reminder_time)) == True:
        result = "past"
    elif (time_parse(now) < time_parse(reminder_time)) == True:
        result = "future"
    elif (time_parse(now) == time_parse(reminder_time)):
        result = "past"
    else:
        result = "unable to compare"

    return result

def update_timer(reminder_id):
    database = "raids_sql.db"
    conn = sql_connect(database)

    def update_sent(reminder_id):
        sql = """   UPDATE timers 
                    SET sent = 1 
                    WHERE id = ?"""
        cur = conn.cursor()
        cur.execute(sql, (reminder_id,))
        conn.commit()

    with conn:
        update_sent(str(reminder_id))


def reminder_check():
    reminders = get_timers()
    ping_messages = []
    now = datetime.now()

    try:
        for x in range(0,len(reminders)):
            reminder_id = reminders[x][0]
            discord_id = reminders[x][1]
            reminder_type = reminders[x][2]
            reminder_item = reminders[x][3]
            reminder_time = reminders[x][5]

            if compare_time(reminder_time) == "past":
                ping_messages.append(str(ping_create(reminder_id, discord_id, reminder_type, reminder_item)))
                update_timer(reminder_id)
                print("updated")
            elif compare_time(reminder_time) == "future":
                print("Time for timer id: " + str(reminder_id) + " is in the future.")
            else:
                print("Unable to compare times for this reminder.")
        print("Sending the below pings: \n----------------------------")
        return ping_messages

    except:
        print("unable to assign sql rows to message params")
        return "E"




if __name__ == '__main__':
    # timer_parse("_timer magic", 80085)

    update_timer(2)

    for reminder in reminder_check():
        print(reminder)
    print("----------------------------\n\n")