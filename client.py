"""
coded by: Roi Tzadok
version: 1.0
date:4.4.2017
a simple client that is able to communicate with the server
"""
import shutil
import os
import urllib2
import socket
import numpy
import platform
import webbrowser
import zipfile

MY_PLATFORM = platform.system()
BUFF_SIZE = numpy.getbufsize()


def unzip(file_path, file_dst):
    """
    unzip a nupkg file
    @param file_path: the zip file path
    @param file_dst: where to unzip to
    """
    zip_ref = zipfile.ZipFile(file_path)
    zip_ref.extractall(file_dst)
    zip_ref.close()


def try_to_download_from_choco(client_socket, file_name):
    """
    after the server database lacked the url we
    try to get it through CHOCO.
    @param file_name: the download's name
    @param client_socket: pass it to add_to_database
    """
    req = urllib2.Request(url='http://chocolatey.org/api/v2/package/' +
                              file_name)
    f = urllib2.urlopen(req)
    file = open(file_name + ".nupkg", "wb+")
    file.write(f.read())
    file.close()
    unzip(file_name + ".nupkg", file_name)
    os.remove(file_name + ".nupkg")
    url_file_dir = os.getcwd() + "\\" + file_name + r"\tools\chocolateyInstall"
    os.rename(url_file_dir + ".ps1", url_file_dir + ".txt")
    file = open(url_file_dir + ".txt", "r")
    content = file.read()
    file.close()
    content = content.split("\n")
    url_lines = []
    for line in content:
        if "url" in line:
            url_lines.append(line)
    url = url_lines[0].split("'")[1]
    webbrowser.open(url)
    add_to_database(file_name, url, MY_PLATFORM, "CHOCO", client_socket)
    # remove the unrared directory
    shutil.rmtree(file_name)


def create_connection(ip, port):
    """
    create connection with the server
    return the socket that was created
    """
    client_socket = socket.socket()
    server_add = (ip, port)
    client_socket.connect(server_add)
    return client_socket


def main():
    client_socket = create_connection("127.0.0.1", 20)
    # whatever you want to send to the server
    data_to_send = raw_input("enter whatever you want to send to the server ")
    if data_to_send == "add":
        data_to_send += " " + raw_input("enter download_name ")
        data_to_send += "," + raw_input("enter url ")
        data_to_send += "," + raw_input("enter platform ")
        data_to_send += "," + raw_input("enter website,"
                                        " you can leave it empty ")
        if data_to_send[-1] == ',':
            data_to_send = data_to_send[:-1]
    else:
        data_to_send += " " + MY_PLATFORM
    # send it to the server
    print data_to_send
    client_socket.send(data_to_send)
    data = client_socket.recv(BUFF_SIZE)
    # check whether the server had the url
    if data[:2] == "ok":
        data = data[2:]
        # start downloading
        webbrowser.open(data)
    elif data[:5] == "CHOCO":
        data = data[5:]
        print data
        file_name = data.split("/")[-1]
        try:
            try_to_download_from_choco(client_socket, file_name)
            data = client_socket.recv(BUFF_SIZE)
            print data
        except urllib2.HTTPError:
            print "sorry, neither the server nor CHOCO had the download for u"
    else:
        print data
    client_socket.close()


def add_to_database(download_name, url, platform, website, client_socket):
    """
    after taking the url from other website
    return the url to the server's database
    @param download_name: the name of the
    application that you want to download
    @param url the new url
    @param platform: your platform (windows,mac...)
    @param website: the website from which the
    download was taken from
    @param client_socket: the socket to which
    we send the new url
    """
    data_to_send = "add " + download_name + "," + url + \
                   "," + platform + "," + website
    client_socket.send(data_to_send)


if __name__ == '__main__':
    main()
