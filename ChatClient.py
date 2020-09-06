#!/usr/bin/env python3
import socket
import sys
import tkinter as tk
from threading import Event, Thread
from tkinter import filedialog
from PIL import Image
import Logging
import FileReader
from Constants import MessageType
from Constants import ClientStatus
from WriterAndReader import WriterAndReader
import io
import time
import psutil

logger = Logging.getLogger('client')
chatLogger = Logging.getChatLogger('chat')
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12346  # The port used by the server
TYPE_OF_STATUS = 0
LENGHT_OF_MESSAGE =1

if len(sys.argv) < 2:
    logger.info('Error! Need a this client name argument as arg #1!')
    exit(14)
name = sys.argv[1]


class CommandProcessor:
    def __init__(self):
        self.buffer = b''
        self.type = None
        self.len = 0

    def clientNewChunk(self, chunk: bytes):
        if self.buffer == b'':
            reader = WriterAndReader()
            chunkArray = bytearray(chunk)
            mesType = reader.parseMessageType(chunkArray)
            mesLen = reader.parseLen(chunkArray)
            mesBody = reader.parseMessage(mesType, chunkArray)
            if (len(mesBody) + len(self.buffer)) < mesLen:
                logger.info('len(mesBody) = {},len(buffer) = {}, mesLen = {}'.format(len(mesBody), len(self.buffer), mesLen))
                self.buffer += mesBody
                self.len = mesLen
                self.type = mesType
            else:
                logger.info('len(mesBody) = {},len(buffer) = {}, mesLen = {}'.format(len(mesBody), len(self.buffer), mesLen))
                self.buffer = b''
                self.len = 0
                self.type = None
                if not self.onCommandClient(mesType, mesBody):
                    return False
        else:
            mesBody = bytearray(chunk)
            if (len(mesBody) + len(self.buffer)) < self.len:
                logger.info('len(mesBody) = {},len(buffer) = {}, mesLen = {}'.format(len(mesBody), len(self.buffer), self.len))
                self.buffer += mesBody
            else:
                logger.info('len(mesBody) = {},len(buffer) = {}, mesLen = {}'.format(len(mesBody), len(self.buffer), self.len))
                self.buffer+=mesBody
                if not self.onCommandClient(self.type, self.buffer):
                    return False
                else:
                    self.buffer = b''
                    self.len = 0
                    self.type = None
        return True

    def onCommandClient(self, messageType: MessageType, messageBody: bytes) -> bool:
        if messageType == MessageType.CLIENTS_ONLINE.value:
            if messageBody == b'':
                chatLogger.info('nobody here')
            else:
                messageBody = messageBody.decode('UTF-8')
                clientsOnline = messageBody.split(',')
                chatLogger.info('these clients are online now:')
                for client in clientsOnline:
                    if client != '':
                        chatLogger.info(client)
        elif messageType == MessageType.STATUS.value:
            status = int(chr(messageBody[TYPE_OF_STATUS]))
            messageBody = messageBody[LENGHT_OF_MESSAGE:]
            messageBody = messageBody.decode('UTF-8')
            if status == ClientStatus.OFFLINE.value:
                chatLogger.info(messageBody + ' offline')
            elif status == ClientStatus.ONLINE.value:
                chatLogger.info(messageBody + ' online')
        elif messageType == MessageType.TEXT.value or messageType == MessageType.TEXT_TO_CLIENT.value:
            messageBody = messageBody.decode('UTF-8')
            chatLogger.info(messageBody)
        elif messageType == MessageType.IMAGE.value:
            img = Image.open(io.BytesIO(messageBody))
            img.show()
        return True

class ListenerThread(Thread):
    def __init__(self, processor: CommandProcessor, s: socket):
        Thread.__init__(self, name='listener thread', daemon=True)
        self.processor = processor
        self.s = s

    def run(self):
        try:
           while True:
                receivedData = self.s.recv(1024)
                if not receivedData:
                    return
                if not self.processor.clientNewChunk(receivedData):
                    return
        except ConnectionResetError:
            logger.info('server closed connection, please reconnect to server latter')
        except:
            logger.info('error', exc_info=True)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    writer = WriterAndReader()
    forSend = writer.createMessage(msgType=MessageType.CLIENT_NAME, msg=bytearray(name,'UTF-8'))
    s.sendall(forSend)
    listenThread = ListenerThread(CommandProcessor(), s)
    listenThread.start()
    toClient = ''
    chatLogger.info('If you want send message to someone enter "name: message" and press enter, if you want send message to everyone enter message without name')
    root = tk.Tk()
    root.withdraw()
    while True:
        try:
            msg = input('')
            if 'picture:' in msg:
                chatLogger.info('please select a picture')
                filePath = filedialog.askopenfilename()
                if not filePath:
                    continue
                bytesPicture = b''
                for bc in FileReader.bytesChunkFromFile(filePath):
                    bytesPicture+=bc
                forSend = writer.createMessage(MessageType.IMAGE, bytesPicture)
                s.sendall(forSend)
            elif ':' in msg:
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
                    forSend = writer.createMessage(MessageType.TEXT, bytearray(msg,'UTF-8'))
                    s.sendall(forSend)
                else:
                    forSend = writer.createMessage(MessageType.TEXT_TO_CLIENT, bytearray(msg,'UTF-8'))
                    s.sendall(forSend)
            elif msg == 'exit':
                forSend = writer.createMessage(MessageType.EXIT,bytearray())
                s.sendall (forSend)
                break
            else:
                forSend = writer.createMessage(MessageType.TEXT, bytearray(msg, 'UTF-8'))
                s.sendall(forSend)
        except ConnectionResetError:
            chatLogger.info('server closed connection, please reconnect to server latter')
        except:
            logger.info('error',exc_info=True)

    logger.info('Finish client on %s:%s' % (HOST, PORT))
