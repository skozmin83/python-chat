#!/usr/bin/env python3
import sys
import socket
import Logging
from threading import Thread
logger = Logging.getLogger('error')
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12346        # The port used by the server

if len(sys.argv)<2:
    logger.info('Error! Need a this client name argument as arg #1!')
    exit(14)
name = sys.argv[1]
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'name:' +bytes(name,'UTF-8')+ b';')
    class newThread (Thread):
        def __init__(self):
            Thread.__init__(self, name='listener thread', daemon = True)

        def run(self):
            while True:
                receivedData = s.recv(1024)
                receivedData = receivedData.decode('UTF-8')
                logger.info('Received: ' + receivedData)
    listenThread = newThread()
    listenThread.start()
    toClient =''
    while True:
        msg = input('enter name: message'+ '\n')
        if ':' in msg:
            toClient, ignored, messageBody = msg.partition(':')
            s.sendall(b'msg-to-client:' + bytes(toClient, 'UTF-8') + b':' + bytes(messageBody, 'UTF-8') + b';')
        elif msg =='exit':
            break
        else:
            messageBody = msg
            s.sendall(b'msg:' + bytes(messageBody, 'UTF-8') + b';')
        if toClient =='':
            logger.info('Connecting client to {}:{} as client {} (talking to everyone)'.format(HOST, PORT, name))
        else:
            logger.info('Connecting client to {}:{} as client {} (talking to {})'.format(HOST, PORT, name, toClient))

    logger.info('Finish client on %s:%s' % (HOST, PORT))

