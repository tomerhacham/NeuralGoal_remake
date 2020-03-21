import socket
import threading
from Server.protocol import protocol

bind_ip = '127.0.0.1'
bind_port = 7777

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(4)  # max backlog of connections

print (('Listening on {}:{}').format(bind_ip, bind_port))


def handle_client_connection(client_socket):
    client_socket.send('Connected'.encode())
    _protocol = protocol()
    while _protocol.terminate==False:
        request = client_socket.recv(1024)
        print (('Received {}').format(request))
        response=_protocol.execute(request.decode('utf-8'))
        client_sock.send(response.encode())
    client_socket.close()


while True:
    client_sock, address = server.accept()
    print (('Accepted connection from {}:{}').format(address[0], address[1]))
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
    )
    client_handler.start()