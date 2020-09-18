#!/usr/bin/env python3
import socket
import sys
import tkinter as tk
from threading import Thread
from PIL import Image
import Logging
from Constants import MessageType
from Constants import ClientStatus
from WriterAndReader import WriterAndReader
import io
from CreatePicture import CreatePicture
from CreateText import CreateText
from threading import RLock
from collections import deque

logger = Logging.getLogger('client')
chatLogger = Logging.getChatLogger('chat')
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12346  # The port used by the server
TYPE_OF_STATUS = 0
LENGHT_OF_MESSAGE =1
LOCK = RLock()

if len(sys.argv) < 2:
    logger.info('Error! Need a this client name argument as arg #1!')
    exit(14)
name = sys.argv[1]


class CommandProcessor:
    def __init__(self):
        self.buffer = b''
        self.type = None
        self.len = 0
        self.alive = True
        self.lock = RLock()
        self.breakFromLoop = False

    def setAlive(self, live: bool):
        if live == True:
            self.alive = True
        else:
            self.alive = False

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
        breakFromListenerLoop = False
        while True:
            receivedData = None
            try:
               while True:
                    receivedData = self.s.recv(1024)
                    if not receivedData:
                        return
                    if not self.processor.clientNewChunk(receivedData):
                        return
                    with self.processor.lock:
                        if self.processor.alive == False:
                            breakFromListenerLoop = True
                            break
                    if breakFromListenerLoop == True:
                        break
            except ConnectionResetError:
                logger.info('server closed connection')
                breakFromListenerLoop = True
                with self.processor.lock:
                    self.processor.breakFromLoop = True
                with self.processor.lock:
                    self.processor.setAlive(False)
                    break
            except:
                logger.info('error', exc_info=True)
                breakFromListenerLoop = True
                break
            if breakFromListenerLoop == True:
                break
        if receivedData != None:
            self.processor.clientNewChunk(receivedData)



class CreateSocket():

    def createSocket (self, host: str, port: int, name: str):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        writer = WriterAndReader()
        forSend = writer.createMessage(msgType=MessageType.CLIENT_NAME, msg=bytearray(name,'UTF-8'))
        s.sendall(forSend)
        return s

    def createListenerThread (self, s:socket):
        cp = CommandProcessor()
        listenThread = ListenerThread(cp,s)
        listenThread.start()

class Main():

    def __init__ (self):
        self.s = None

    def mainChatFunction (self, savedMessage: deque):
        createS = CreateSocket()
        s = createS.createSocket(HOST, PORT, name)
        createS.createListenerThread(s)
        self.s = s
        # chatLogger.info('If you want send message to someone enter "name: message" and press enter, if you want send message to everyone enter message without name')
        # chatLogger.info('If you want send picture to someone enter "name: picture:" and press enter, if you want send picture to everyone press enter without name')
        root = tk.Tk()
        root.withdraw()
        processor = CommandProcessor()
        with processor.lock:
            self.breakFromLoop = False
        while len(savedMessage)>0:
            newMsg = savedMessage.popleft()
            self.processingMessage(newMsg)
        with processor.lock:
            processor.setAlive(True)
        msg = None
        while True:
            while True:
                try:
                    with processor.lock:
                        if processor.alive == False:
                            break
                        if processor.breakFromLoop == True:
                            break
                    msg = input('')
                    if msg != '':
                       self.processingMessage(msg)
                    with processor.lock:
                        if self.breakFromLoop == True:
                            break
                except ConnectionResetError:
                    if msg != None:
                        savedMessage.append(msg)
                        logger.info('server closed connection')
                    try:
                        with processor.lock:
                            processor.setAlive(False)
                    finally:
                        self.breakFromLoop = True
                        break
                except:
                    logger.info('error',exc_info=True)
                    with processor.lock:
                        self.breakFromLoop = True
                        break
                with processor.lock:
                    if self.breakFromLoop == True:
                        break
            with processor.lock:
                if processor.alive == False:
                    s.close()
                    nextMain = Main()
                    nextMain.mainChatFunction(savedMessage)
            logger.info('Finish client on %s:%s' % (HOST, PORT))


    def processingMessage(self, msg: str):
        writer = WriterAndReader()
        if 'picture:' in msg:
            create = CreatePicture()
            toClient = create.nameOfReceiver(msg)
            chatLogger.info('please select a picture')
            pathToPicture = create.openPicture()
            if pathToPicture == False:
                pass
            if toClient == False:
                forSend = create.sendPicture(pathToPicture)
            else:
                forSend = create.sendPicToClient(toClient, pathToPicture)
            self.s.sendall(forSend)
        elif ':' in msg:
            create = CreateText()
            forSend = create.determineNameOfClient(msg)
            self.s.sendall(forSend)
        elif msg == 'exit':
            forSend = writer.createMessage(MessageType.EXIT, bytearray())
            self.s.sendall(forSend)
            processor = CommandProcessor()
            with processor.lock:
                self.breakFromLoop = True
        else:
            forSend = writer.createMessage(MessageType.TEXT, bytearray(msg, 'UTF-8'))
            self.s.sendall(forSend)
main = Main()
main.mainChatFunction(deque())