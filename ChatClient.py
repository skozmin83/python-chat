#!/usr/bin/env python3

import sys
import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12346        # The port used by the server

if len(sys.argv) < 2:
    print("Error! Need a client name argument!")
    exit(15)

clientName = sys.argv[1]

print('Connecting client to {}:{} as client {}'.format(HOST, PORT, clientName))
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'name:' + bytes(clientName, "UTF-8") + b';')
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
