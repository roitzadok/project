"""
coded by: Roi Tzadok
version: 1.0
date:4.4.2017
database creation and management
"""
import sqlite3
import os


DATABASE_FILE = "database.db"


class DataBase:
    """
    creates the database and control it
    """

    def get_url_list(self, download_name):
        """
        return the urls for your app
        @param download_name: the name of the
        application that you want to download
        """
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT url FROM downloads_websites_urls"
                       " WHERE download_name = '%s'" % download_name)
        # get a list
        lst = cursor.fetchall()
        # close the file
        conn.close()
        return lst

    def get_the_best_url(self, url_list, platform):
        """
        out of a given list return the best rated url for your platform
        @param platform: your platform (windows,mac...)
        @param url_list: the given list
        """
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        relevant_urls = []
        cursor.execute("SELECT url FROM urls_devices_rating"
                       " ORDER BY rating_number_of_people")
        all_urls = cursor.fetchall()
        for url in all_urls:
            cursor.execute("SELECT device_or_devices FROM"
                           " urls_devices_rating WHERE url='%s'" % url)
            url = url[0]
            platform_lst = cursor.fetchall()[0][0].split(",")
            if platform in platform_lst and url in url_list:
                relevant_urls.append(url)
        relevant_urls = relevant_urls[::-1]
        try:
            return relevant_urls[0]
        # the list is empty
        except IndexError:
            return 0

    def get_url(self, download_name, platform):
        """
        use get_best_url and url_list in order to give the user the right url
        @param download_name: the name of the
        application that you want to download
        @param platform: your platform (windows,mac...)
        return whether the database contains
        the application or even the url itself
        """
        try:
            url_list = self.get_url_list(download_name)[0][0]
        # the list is empty
        except IndexError:
            return "no urls for that application, sorry"
        url_list = url_list.split(',')
        best_url = self.get_the_best_url(url_list, platform)
        if best_url == 0:
            return "no urls for your platform, sorry"
        return "ok" + best_url

    def create_first_table(self):
        """
        create a table
        """
        self.cursor.execute("""
            CREATE TABLE downloads_websites_urls
                        (download_name TEXT PRIMARY KEY,
                         website_name TEXT,url TEXT)
            """)

    def create_second_table(self):
        """
        create a table
        """
        self.cursor.execute("""
            CREATE TABLE urls_devices_rating
                        (url TEXT PRIMARY KEY, device_or_devices TEXT,
                         rating_number_of_people)
            """)

    def add_to_table(self, download_name, url, platform, website=None):
        """
        add to both tables the new download
        @param download_name: the name of the
        application that you want to download
        @param url the new url
        @param platform: your platform (windows,mac...)
        @param website: the website from which the
        download was taken from
        """
        conn = sqlite3.connect(DATABASE_FILE)
        self.cursor = conn.cursor()
        if website is None:
            website = ""
        try:
            self.cursor.execute("INSERT INTO downloads_websites_urls "
                                "VALUES ('%s','%s','%s,')"
                                % (download_name, website, url))
            self.cursor.execute("INSERT INTO urls_devices_rating "
                                "VALUES ('%s','%s','5,1')" % (url, platform))
        except sqlite3.IntegrityError:
            current_url = self.cursor.execute("SELECT url "
                                              "FROM downloads_"
                                              "websites_urls WHERE "
                                              "download_name='%s'"
                                              % download_name)
            new_url = current_url.fetchall()[0][0] + url + ","
            if not website:
                website = self.cursor.execute("SELECT website_name "
                                              "FROM downloads_"
                                              "websites_urls WHERE "
                                              "download_name='%s'"
                                              % download_name)
                website = website.fetchall()[0][0]
            self.cursor.execute("UPDATE downloads_websites_urls"
                                " SET website_name='%s',"
                                " url='%s' WHERE download_name='%s'"
                                % (website, new_url, download_name))
            self.cursor.execute("INSERT INTO urls_devices_rating "
                                "VALUES ('%s','%s','5,1')"
                                % (new_url, platform))
        conn.commit()
        conn.close()

    def __init__(self):
        if not os.path.exists(DATABASE_FILE):
            conn = sqlite3.connect(DATABASE_FILE)
            self.cursor = conn.cursor()
            # create table
            self.create_first_table()
            # create table
            self.create_second_table()
            conn.commit()
            # close the file
            conn.close()
            self.add_to_table("python",
                              "https://www.python.org/ftp/python"
                              "/2.7.13/python-2.7.13.msi",
                              "Windows", "https://www.python.org")

    def print_table(self, table_name):
        """
        print a sql table
        @param table_name: the table you would like to print
        """
        conn = sqlite3.connect(DATABASE_FILE)
        self.cursor = conn.cursor()
        self.cursor.execute("SELECT * FROM %s" % table_name)
        print(self.cursor.fetchall())
        conn.close()
