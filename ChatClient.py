#!/usr/bin/env python3
import sys
import socket
import Logging
from PIL import Image
import tkinter as tk
from tkinter import filedialog
from threading import Event, Thread
import codecs
import io
import sys

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
        try:
            while True:
                receivedData = s.recv(1024)
                if receivedData:
                    self.clientNewChunk(receivedData)
        except:
            logger.info('error', exc_info=True)

    def clientNewChunk (self, chunk: bytes):
        self.buffer += chunk
        while True:
            if b';;' not in self.buffer:
                break
            message, ignored, self.buffer = self.buffer.partition(b';;')
            messageType, ignored, messageBody = message.partition(b':')
            if messageType ==b'pic':
                fromClient, ignor, messageBody = messageBody.partition(b':')
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
        elif messageType == b'pic':
            size = 512,512
            img = Image.frombytes(decoder_name='raw',size=size,data=messageBody, mode='RGB')
            img.show()
        return True
event = Event()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    event.set()
    s.connect((HOST, PORT))
    s.sendall(b'name:' + bytes(name, 'UTF-8') + b';;')
    listenThread = ListenerThread()
    listenThread.start()
    toClient = ''
    chatLogger.info('If you want send message to someone enter "name: message" and press enter, if you want send message to everyone enter message without name')
    chatLogger.info('If you want send picture to someone enter "name: picture:" and press enter, if you want send picture to everyone enter "picture:" withont name')
    root = tk.Tk()
    root.withdraw()
    while True:
        i = True
        msg = input('')
        if 'picture:' in msg:
            # image = Image.open('C:/Users/11/Desktop/Снимок.png')
            # image.show()
            # root = tk.Tk()
            file = filedialog.askopenfilename()
            openFileObj = open(file,encoding='latin1')
            read = bytes(openFileObj.read(1024), 'UTF-8')
            s.sendall(b'pic:'+ read)
            while (read):
                read = bytes(openFileObj.read(1024),'UTF-8')
                s.sendall(read)
            else:
                s.sendall(b';;')
        if ':' in msg:
            firstValue = msg[0]
            secondValue = msg[1]
            try:
                int(firstValue)
                itIsName = False
            except:
                try:
                    int(secondValue)
                    itIsName = False
                except:
                    itIsName = True
            if msg[0] == ':' or itIsName == False:
                    messageBody = msg
                    s.sendall(b'msg:' + bytes(messageBody, 'UTF-8') + b';;')
            else:
                toClient, ignored, messageBody = msg.partition(':')
                s.sendall(b'msg-to-client:' + bytes(toClient, 'UTF-8') + b':' + bytes(messageBody, 'UTF-8') + b';;')
        elif msg == 'exit':
            break
        else:
            messageBody = msg
            s.sendall(b'msg:' + bytes(messageBody, 'UTF-8') + b';;')
        if toClient == '':
            logger.info('Connecting client to {}:{} as client {} (talking to everyone)'.format(HOST, PORT, name))
        else:
            logger.info('Connecting client to {}:{} as client {} (talking to {})'.format(HOST, PORT, name, toClient))

    logger.info('Finish client on %s:%s' % (HOST, PORT))


# def insertImage():
#     fileName = filedialog.askopenfilename()
#     file = open(fileName)
    # save = file.read()
    # file.close()
    # return save

#
# from PIL import Image
#
# image = Image.open('C:/Users/sergey/Desktop/umbrella.psd')
# image.show()import tkinter as tk
# from tkinter import filedialog
# from PIL import Image
#
# root = tk.Tk()
# root.withdraw()
