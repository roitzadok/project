import socket
import numpy
import platform
import webbrowser


MY_PLATFORM = platform.system()
BUFF_SIZE = numpy.getbufsize()


def main():
    client_socket = socket.socket()
    server_add = ('127.0.0.1', 20)
    client_socket.connect(server_add)
    data_to_send = raw_input("enter whatever you want to send to the server ") + " " + MY_PLATFORM
    client_socket.send(data_to_send)
    data = client_socket.recv(BUFF_SIZE)
    if data[:2] == "ok":
        data = data[2:]
        webbrowser.open(data)
    else:
        print data


if __name__ == '__main__':
    main()