#!/usr/bin/env python3

import sys
import socket
import Logging
logger = Logging.getLogger('error')
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12346        # The port used by the server
if len(sys.argv)<2:
    logger.info('Error! Need a this client name argument as arg #1!')
    exit(14)
if len(sys.argv) < 3:
    logger.info('Error! Need an another client name as arg #2')
    exit(15)

clientName = sys.argv[1]
toClient = sys.argv[2]


logger.info('Connecting client to {}:{} as client {} (talking to {})'.format(HOST, PORT, clientName, toClient))
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'name:' + bytes(clientName, "UTF-8") + b';')
    s.sendall(b'msg:Hi;')
    s.sendall(b'msg-to-client:' + bytes(toClient, "UTF-8") + b':test message;')
    while True:
        receivedData = s.recv(1024)
        logger.info('Received:', repr(receivedData))
        if not receivedData:
            break
logger.info('Finish client on %s:%s' % (HOST, PORT))
