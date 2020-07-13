#!/usr/bin/env python3
import sys
import socket
import Logging
import ClientStatus
import time
from threading import Event, Thread

logger = Logging.getLogger('client')
chatLogger = Logging.getChatLogger('chat')
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12346  # The port used by the server

if len(sys.argv) < 2:
    logger.info('Error! Need a this client name argument as arg #1!')
    exit(14)
name = sys.argv[1]

class ListenerThread(Thread):
    def __init__(self):
        Thread.__init__(self, name='listener thread', daemon=True)
        self.buffer = b''

    def run(self):
        while not event.isSet():
            if event.isSet():
                break
        while event.isSet():
            receivedData = s.recv(1024)
            if receivedData:
                chatLogger.info(receivedData.decode('UTF-8'))
                event.clear()
                self.clientNewChunk(receivedData)
    def clientNewChunk (self, chunk: bytes):
        self.buffer += chunk
        while True:
            if b';' not in self.buffer:
                break
            message, ignored, self.buffer = self.buffer.partition(b';')
            messageType, ignored, messageBody = message.partition(b':')
            if not self.onCommandClient(messageType, messageBody):
                return False
        return True

    def onCommandClient(self, messageType: bytes, messageBody: bytes) -> bool:
        if messageType == b'clients':
            messageBody = messageBody.decode('UTF-8')
            clientsOnline = messageBody.split(' ')
            if clientsOnline[0] !='':
                chatLogger.info('these clients are online now:')
            else:
                chatLogger.info('nobody here')
            for client in clientsOnline:
                if client !='':
                    chatLogger.info(client)
        elif messageType == b'status-update':
            messageBody = messageBody.decode('UTF-8')
            chatLogger.info(messageBody)
        elif messageType == b'msg':
            messageBody = messageBody.decode('UTF-8')
            chatLogger.info(messageBody)
        # event.set()
        return True
event = Event()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    event.set()
    s.connect((HOST, PORT))
    s.sendall(b'name:' + bytes(name, 'UTF-8') + b';')
    listenThread = ListenerThread()
    listenThread.start()
    while not event.isSet():
        chatLogger.info('waiting')
        if event.isSet():
            break
    toClient = ''
    chatLogger.info('If you want send message to someone enter "name: message", if you want send message to everyone enter message without name')
    while event.isSet():
        msg = input('type something...' + '\n')
        if ':' in msg:
            toClient, ignored, messageBody = msg.partition(':')
            s.sendall(b'msg-to-client:' + bytes(toClient, 'UTF-8') + b':' + bytes(messageBody, 'UTF-8') + b';')
        elif msg == 'exit':
            break
        else:
            messageBody = msg
            s.sendall(b'msg:' + bytes(messageBody, 'UTF-8') + b';')
        if toClient == '':
            logger.info('Connecting client to {}:{} as client {} (talking to everyone)'.format(HOST, PORT, name))
        else:
            logger.info('Connecting client to {}:{} as client {} (talking to {})'.format(HOST, PORT, name, toClient))

    logger.info('Finish client on %s:%s' % (HOST, PORT))
