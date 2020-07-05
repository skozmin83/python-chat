#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12346        # The port used by the server

print('Connecting client to %s:%s' % (HOST, PORT))
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'name:tanya;')
    s.sendall(b'msg:Hi;')
    data = s.recv(1024)
    s.listen(5)
    conn, addr = s.accept()
with conn:
    while True:
        receivedData = conn.recv(1024)
        print('received:', repr(receivedData) )
        if not receivedData:
            break

print('Received: ', repr(data))
print('Finish client on %s:%s' % (HOST, PORT))
