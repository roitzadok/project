"""
coded by: Roi Tzadok
version: 1.0
date:4.4.2017
a simple client that is able to communicate with the server
"""
import socket
import numpy
import platform
import webbrowser


MY_PLATFORM = platform.system()
BUFF_SIZE = numpy.getbufsize()


def main():
    # create connection
    client_socket = socket.socket()
    server_add = ('127.0.0.1', 20)
    client_socket.connect(server_add)
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
    else:
        print data


if __name__ == '__main__':
    main()
