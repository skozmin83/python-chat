#!/usr/bin/env python3
import sys
import socket
import Logging
# import ChatServer
logger = Logging.getLogger('error')
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12346        # The port used by the server

if len(sys.argv)<2:
    logger.info('Error! Need a this client name argument as arg #1!')
    exit(14)
name = sys.argv[1]
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = s.recv(1024)
    data = data.decode('UTF-8')
    logger.info(data)
    toClient =''
    messageBody =''
    msg = input('enter name: message')
    if ':' in msg:
        toClient, ignored, messageBody = msg.partition(':')
    else:
        messageBody = msg
    if toClient =='':
        logger.info('Connecting client to {}:{} as client {} (talking to everyone)'.format(HOST, PORT, name))
    else:
        logger.info('Connecting client to {}:{} as client {} (talking to {})'.format(HOST, PORT, name, toClient))
    s.sendall(b'name:' +bytes(name,'UTF-8')+ b';')
    # receivedData = s.recv(1024)
    # receivedData = receivedData.decode('UTF-8')
    # logger.info('Received:' + receivedData)
    while True:
        if messageBody !='' and toClient !='':
            s.sendall(b'msg-to-client:'+bytes(toClient,'UTF-8')+ b':' + bytes(messageBody, 'UTF-8') + b';')
            messageBody =''
            toClient =''
            msg = input('enter name: message')
        elif messageBody !='' and toClient =='':
            s.sendall(b'msg:' + bytes(messageBody, 'UTF-8') + b';')
            msg = input('enter name: message')
        elif messageBody == '' and toClient == '':
            break
        if ':' in msg:
            toClient, ignored, messageBody = msg.partition(':')
        else:
            messageBody = msg
    while True:
        receivedData = s.recv(1024)
        receivedData = receivedData.decode('UTF-8')
        logger.info('Received: ' + receivedData)
        if not receivedData:
            break
logger.info('Finish client on %s:%s' % (HOST, PORT))

