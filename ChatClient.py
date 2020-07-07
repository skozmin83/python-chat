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
name = sys.argv[1]
msg = input('your message is')
msg_to = input('your message for:')
logger.info('Connecting client to {}:{} as client {} (talking to {})'.format(HOST, PORT, name, msg_to))
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'name:' +bytes(name,'UTF-8')+ b';')
    s.sendall(b'msg:'+bytes(msg, 'UTF-8')+ b';')
    s.sendall(b'msg-to-client:'+bytes(msg_to,'UTF-8')+ b':' + bytes(msg, 'UTF-8') + b';')
    while True:
        receivedData = s.recv(1024)
        logger.info('Received:' + str(receivedData))
        if not receivedData:
            break
logger.info('Finish client on %s:%s' % (HOST, PORT))
