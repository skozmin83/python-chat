#!/usr/bin/env python3

import sys
import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12346        # The port used by the server

if len(sys.argv) < 3:
    print("Error! Need a this client name argument as arg #1!")
    print("Error! Need a another client name name argument as arg #2!")
    exit(15)

clientName = sys.argv[1]
toClient = sys.argv[2]

print('Connecting client to {}:{} as client {} (talking to {})'.format(HOST, PORT, clientName, toClient))
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'name:' + bytes(clientName, "UTF-8") + b';')
    s.sendall(b'msg:Hi;')
    s.sendall(b'msg-to-client:' + bytes(toClient, "UTF-8") + b':test message;')
    while True:
        receivedData = s.recv(1024)
        print('Received:', repr(receivedData))
        if not receivedData:
            break

print('Finish client on %s:%s' % (HOST, PORT))
