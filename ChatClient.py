#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12346        # The port used by the server

print('Connecting client to %s:%s' % (HOST, PORT))
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    s.sendall(b'name:sergey;')
    # counter = 0
    # while counter < 1_000_000:
    #     msg = 'msg:msg#{};'.format(counter)
    #     b = bytes(msg, "UTF-8")
    #     s.sendall(b)
    #     counter += 1

    s.sendall(b'msg:hello from client;')
    s.sendall(b'msg-to-client:tanya:hello3;')
    s.sendall(b'exit:;')
    data = s.recv(1024)

print('Received: ', repr(data))
print('Finish client on %s:%s' % (HOST, PORT))
