import socket
import numpy


BUFF_SIZE = numpy.getbufsize()

def main():
    client_socket = socket.socket()
    server_add = ('127.0.0.1', 20)
    client_socket.connect(server_add)
    client_socket.send(raw_input("enter whatever you want to send to the server "))
    data=client_socket.recv(BUFF_SIZE)
    print data


if __name__ == '__main__':
    main()