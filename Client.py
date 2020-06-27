#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12345        # The port used by the server

print('Connect client to %s:%s' % (HOST, PORT))
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'This is Sergey')
    data = s.recv(1024)

print('Received: ', repr(data))
print('Finish client on %s:%s' % (HOST, PORT))