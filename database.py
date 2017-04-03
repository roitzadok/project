import sqlite3
import os


class DataBase:
    def get_url(self,download_name):
        print download_name
        return "somthing"
    def __init__(self):
        if not os.path.exists("database.db"):
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            # create table
            cursor.execute("""
            CREATE TABLE downloads_websites
                        (download_name TEXT PRIMARY KEY, website_name TEXT)
            """)
            cursor.execute("INSERT INTO downloads_websites "
                           "VALUES ('python','https://www.python.org')")
            # create table
            cursor.execute("""
            CREATE TABLE websites_
                        (download_name TEXT PRIMARY KEY, website_name TEXT)
            """)
        else:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
        conn.commit()
        print_table(cursor,"downloads_websites")
        conn.close()
        os.remove("database.db")# remove me later!!!!!!!!!!!!!!!!!!!

def print_table(cursor,table_name):
    cursor.execute("SELECT * FROM %s"%(table_name))
    print(cursor.fetchall())
