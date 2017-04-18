"""
coded by: Roi Tzadok
version: 1.0
date:4.4.2017
the server which offers the downloads+main
"""
import database
import socket
import numpy
import select


BUFF_SIZE = numpy.getbufsize()


def send_waiting_messages(wlist, messages_to_send):
    """
    send messages to clients and remove them from the list
    @param wlist: write list
    @param messages_to_send: the staff we need to send
    """
    for message in messages_to_send:
        (client_socket, data) = message
        if client_socket in wlist:
            client_socket.send(data)
            messages_to_send.remove(message)


def server(database):
    """
    communicate with clients and send them downloads
    @param database the database we have
    """
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 20))
    # up to X people
    server_socket.listen(5)
    open_client_sockets = []
    messages_to_send = []
    while True:
        rlist, wlist, xlist = select.select([server_socket] +
                                            open_client_sockets,
                                            open_client_sockets, [])
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
                    if data[:9] == "download ":
                        platform = data.split()[-1]
                        data = data[:-(len(platform) + 1)]
                        data = data[9:]
                        data=data.replace(" ","")
                        url = database.get_url(data, platform)
                        if url[:2]!="ok":
                            url="CHOCO"+"http://chocolatey.org/api/v2/package/"+data
                        print url
                        messages_to_send.append((current_socket, url))
                    elif data[:4] == "add ":
                        data = data[4:]
                        data = data.split(",")
                        print data
                        if len(data) == 4 and "" not in data:
                            database.add_to_table(data[0],
                                                  data[1],
                                                  data[2],
                                                  data[3])
                            messages_to_send.append((current_socket,
                                                     "thank you!"))
                        elif "" not in data:
                            database.add_to_table(data[0], data[1], data[2])
                            messages_to_send.append((current_socket,
                                                     "thank you!"))
                        else:
                            messages_to_send.append((current_socket,
                                                     "you are evil!!!!"))
                        database.print_table("downloads_websites_urls")
                    else:
                        data = "unknown request"
                        messages_to_send.append((current_socket, data))
        send_waiting_messages(wlist, messages_to_send)


def main():
    d = database.DataBase()
    server(d)


if __name__ == '__main__':
    main()
