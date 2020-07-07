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
    logger.info(str(data))
    msg = input('enter your message please')
    msg_to = input('if you want send it as private message, add name of the person, else press Enter')
    logger.info('Connecting client to {}:{} as client {} (talking to {})'.format(HOST, PORT, name, msg_to))
    s.sendall(b'name:' +bytes(name,'UTF-8')+ b';')
    while True:
        if msg_to !='' and msg != '':
            s.sendall(b'msg-to-client:'+bytes(msg_to,'UTF-8')+ b':' + bytes(msg, 'UTF-8') + b';')
            msg =''
        elif msg_to =='' and msg !='':
            s.sendall(b'msg:' + bytes(msg, 'UTF-8') + b';')
            msg_to=''
        elif msg == '' and msg_to !='':
            msg = input('enter your message please')
            msg_to = input('if you want send it as private message, add name of the person, else press Enter')
            continue
        elif msg =='' and msg_to =='':
            break
    while True:
        receivedData = s.recv(1024)
        logger.info('Received:' + str(receivedData))
        if not receivedData:
            break
logger.info('Finish client on %s:%s' % (HOST, PORT))

