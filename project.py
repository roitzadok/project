import database
import webbrowser
import socket
import numpy
import select


BUFF_SIZE = numpy.getbufsize()


def send_waiting_messages(wlist, messages_to_send):
    for message in messages_to_send:
        (client_socket, data) = message
        if client_socket in wlist:
            client_socket.send(data)
            messages_to_send.remove(message)


def server(database):
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 20))
    server_socket.listen(5)
    open_client_sockets = []
    messages_to_send = []
    while True:
        rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, open_client_sockets, [])
        for current_socket in rlist:
            if current_socket is server_socket:
                (new_socket, address) = server_socket.accept()
                open_client_sockets.append(new_socket)
            else:
                data = current_socket.recv(BUFF_SIZE)
                # connection with client closed
                if data == "":
                    open_client_sockets.remove(current_socket)
                else:
                    if data[:9]=="download ":
                        data=data[9:]
                        data=database.get_url(data)
                        messages_to_send.append((current_socket, data))
                    else:
                        data="unknown request"
                        messages_to_send.append((current_socket, data))
        send_waiting_messages(wlist, messages_to_send)


def main():
    d = database.DataBase()
    # webbrowser.open("https://www.python.org/ftp/python/2.7.13/python-2.7.13.msi")
    server(d)

if __name__ == '__main__':
    main()