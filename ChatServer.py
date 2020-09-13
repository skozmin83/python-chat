#!/usr/bin/env python3
import socket
import Logging
import Constants
from threading import Thread
from WriterAndReader import WriterAndReader


class SingleClientCommandProcessor:
    logger = Logging.getChatLogger("processor")

    def __init__(self, clients: dict, conn: socket, ip, port):
        self.conn = conn
        self.clients = clients
        self.ip = ip
        self.port = port
        self.clientName = None
        self.buffer = b''
        self.len = 0
        self.type = None
        self.writer = WriterAndReader()
        self.savedReceiver = b''

    def start(self):
        self.logger.info("start processing commands")
        clientsMsg = b''

        if len(self.clients) > 0:
            clientsMsg = b''
            for client in self.clients.keys():
                if client !=None:
                    clientsMsg += client + b','

        forSend = self.writer.createMessage(Constants.MessageType.CLIENTS_ONLINE, bytearray(clientsMsg))
        self.conn.sendall(forSend)

    def finish(self):
        self.logger.info("finish processing commands")
        self.statusUpdate(self.clientName, Constants.ClientStatus.OFFLINE.value)
        if self.clientName in self.clients:
            del self.clients[self.clientName]

    def processNewChunk(self, chunk: bytes) -> bool:
        if self.buffer ==b'':
            chunkArray = bytearray(chunk)
            mesType = self.writer.parseMessageType(chunkArray)
            if mesType == Constants.MessageType.IMAGE_TO_CLIENT.value:
                nameLen = self.writer.parseLenReceiver(chunkArray)
                mesLen = self.writer.parseLenPicrture(chunkArray)
                mesName = self.writer.parsePictureReceiver(chunkArray,nameLen)
                mesBody = self.writer.parsePicture(chunkArray,nameLen)
                self.savedReceiver = mesName
            else:
                mesLen = self.writer.parseLen(chunkArray)
                mesBody = self.writer.parseMessage(mesType,chunkArray)
            if (len(mesBody)+len(self.buffer))<mesLen:
                self.buffer+=mesBody
                self.len = mesLen
                self.type = mesType
                self.logger.info('len(mesBody) = {},len(buffer) = {}, mesLen = {}'.format(len(mesBody),len(self.buffer), mesLen))
            else:
                self.buffer = b''
                self.len = 0
                self.type = None
                self.logger.info('len(mesBody) = {}, len(buffer) = {}, mesLen = {}'.format(len(mesBody),len(self.buffer), mesLen))
                if not self.onCommand(mesType, mesBody):
                    return False
        else:
            mesBody = bytearray(chunk)
            if (len(mesBody)+len(self.buffer))<self.len:
                self.buffer+=mesBody
                self.logger.info('len(mesBody)  = {}, len(buffer) = {}, mesLen = {}'.format(len(mesBody),len(self.buffer), self.len))
            else:
                self.buffer += mesBody
                if not self.onCommand(self.type, self.buffer):
                    return False
                self.buffer = b''
                self.len = 0
                self.type = None
                self.logger.info('len(mesBody) = {}, len(buffer) = {}, mesLen = {}'.format(len(mesBody),len(self.buffer), self.len))
        return True

    def onCommand(self, command: Constants.MessageType, data: bytes) -> bool:
        self.logger.info("processing command[{}], data[{}]".format(command, data))
        if command == Constants.MessageType.CLIENT_NAME.value:
            self.clientName = data
            self.clients[self.clientName] = self
            self.statusUpdate(self.clientName, Constants.ClientStatus.ONLINE.value)
        elif command == Constants.MessageType.TEXT.value:
            messageBody = data
            self.logger.info("user [{}] says [{}]".format(self.clientName, data))
            for processor in self.clients.values():
                processor.sendMessage(self.clientName, messageBody)
        elif command == Constants.MessageType.TEXT_TO_CLIENT.value:
            toClient, ignored, messageBody = data.partition(b':')
            self.logger.info("from [{}] to [{}] message [{}]".format(self.clientName, toClient, messageBody))
            if toClient in self.clients:
                if self.clients[toClient] != None:
                    self.clients[toClient].sendMessageToClient(self.clientName, messageBody)
                else:
                    toClient = toClient.decode('UTF-8')
                    self.logger.info("client {} left our server and we can't send message to him".format(toClient))
            else:
                self.logger.info("no client [{}] on server".format(toClient))
        elif command == Constants.MessageType.IMAGE.value:
            messageBody = data
            for processor in self.clients.values():
                if processor !=None:
                    processor.sendPic(self.clientName, messageBody)
        elif command == Constants.MessageType.IMAGE_TO_CLIENT.value:
            toClient = self.savedReceiver
            self.savedReceiver = b''
            messageBody = data
            self.logger.info("from [{}] to [{}] picture [{}]".format(self.clientName, toClient, messageBody))
            if toClient in self.clients:
                if self.clients[toClient] != None:
                    self.clients[toClient].sendPic(self.clientName, messageBody)
                else:
                    toClient = toClient.decode('UTF-8')
                    self.logger.info("client {} left our server and we can't send message to him".format(toClient))
            else:
                self.logger.info("no client [{}] on server".format(toClient))
        elif command == Constants.MessageType.EXIT.value:
            del self.clients[self.clientName]
            return False
        else:
            self.logger.info('no such command')
            return False
        return True

    def statusUpdate(self, fromClient, newStatus: Constants):
        if newStatus == Constants.ClientStatus.OFFLINE.value:
            byteStatus = b'1'
        else:
            byteStatus = b'2'
        for processor in self.clients.values():
            if processor != None:
                processor.sendStatusToClient(fromClient, byteStatus)

    def sendStatusToClient(self, fromClient: bytes, status: bytes):
        if self.clientName != fromClient:
            forSend = self.writer.createMessage(Constants.MessageType.STATUS, bytearray(status+fromClient))
            self.conn.sendall(forSend)

    def sendMessageToClient(self, fromClient: bytes, message: bytes):
        forSend = self.writer.createMessage(Constants.MessageType.TEXT_TO_CLIENT,bytearray(fromClient+b':'+ message))
        if self.clientName != fromClient:
            self.conn.sendall(forSend)

    def sendMessage(self, fromClient: bytes, message: bytes):
        forSend = self.writer.createMessage(Constants.MessageType.TEXT, bytearray(fromClient+b': '+ message))
        if self.clientName != fromClient:
            self.conn.sendall(forSend)

    def sendPic(self, fromClient: bytes, pic: bytes):
        forSend = self.writer.createMessage(Constants.MessageType.IMAGE, bytearray(pic))
        if self.clientName != fromClient:
            self.conn.sendall(forSend)


class ClientThread(Thread):
    logger = Logging.getChatLogger("clientThread")
    chatLogger = Logging.getChatLogger('error')

    def __init__(self, processor: SingleClientCommandProcessor, conn: socket):
        Thread.__init__(self, name="t-{}:{}".format(ip, port), daemon=True)
        self.processor = processor
        self.conn = conn

    def run(self):
        try:
            self.processor.start()
            with self.conn:
                while True:
                    data = self.conn.recv(1024)
                    if not data:
                        return
                    if not self.processor.processNewChunk(data):
                        return
        except ConnectionResetError:
            self.logger.info("client closed connection")
        except:
            self.chatLogger.info("unknown error", exc_info=True)
        finally:
            self.logger.info("exiting thread")
            self.processor.finish()


BUFFER_SIZE = 1024

HOST = '127.0.0.1'
PORT = 12346

mainLogger = Logging.getChatLogger("main")

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((HOST, PORT))
threads = []
allClients = {}

mainLogger.info("SERVER: Waiting for connections from TCP clients on {}:{} ...".format(HOST, PORT))
while True:
    tcpServer.listen()
    (connection, (ip, port)) = tcpServer.accept()
    processor = SingleClientCommandProcessor(allClients, connection, ip, port)
    newthread = ClientThread(processor, connection)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()

mainLogger.info("SERVER: Exit")
