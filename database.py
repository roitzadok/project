import sqlite3
import os


DATABASE_FILE="database.db"

class DataBase:
    def get_url(self, download_name):
        print download_name
        return "somthing"

    def __init__(self):
        if not os.path.exists(DATABASE_FILE):
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            # create table
            cursor.execute("""
            CREATE TABLE downloads_websites_urls
                        (download_name TEXT PRIMARY KEY, website_name TEXT,url TEXT)
            """)
            cursor.execute("INSERT INTO downloads_websites_urls "
                           "VALUES ('python','https://www.python.org',"
                           "'https://www.python.org/ftp/python/2.7.13/python-2.7.13.msi,"
                           "https://www.python.org/ftp/python/2.7.13/python-2.7.13-macosx10.6.pkg')")
            # create table
            cursor.execute("""
            CREATE TABLE urls_devices_rating
                        (url TEXT PRIMARY KEY, device_or_devices TEXT, rating_number_of_people)
            """)
            cursor.execute("INSERT INTO urls_devices_rating "
                           "VALUES ('https://www.python.org/ftp/python/2.7.13/python-2.7.13.msi','windows','5,1')")
            cursor.execute("INSERT INTO urls_devices_rating "
                           "VALUES ('https://www.python.org/ftp/python/2.7.13/python-2.7.13-macosx10.6.pkg'"
                           ",'windows','5,1')")
        else:
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
        conn.commit()
        print_table(cursor, "downloads_websites_urls")
        print_table(cursor,"urls_devices_rating")
        conn.close()
        os.remove(DATABASE_FILE)  # remove me later!!!!!!!!!!!!!!!!!!!


def print_table(cursor, table_name):
    cursor.execute("SELECT * FROM %s" % (table_name))
    print(cursor.fetchall())
