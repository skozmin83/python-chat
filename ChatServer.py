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

    def start(self):
        self.logger.info("start processing commands")
        clientsMsg = b'7'
        for client in self.clients.keys():
            if client !=None:
                clientsMsg += client + b' '
        self.conn.sendall(clientsMsg)

    def finish(self):
        self.logger.info("finish processing commands")
        self.statusUpdate(self.clientName, Constants.ClientStatus.OFFLINE.value)
        self.clients[self.clientName] = None

    def processNewChunk(self, chunk: bytes) -> bool:
        reader = WriterAndReader()
        chunkArray = bytearray(chunk)
        mesType = reader.parseMessageType(chunkArray)
        mesLen = reader.parseLen(chunkArray)
        mesBody = reader.parseMessage(mesType,chunkArray)
        if not self.onCommand(mesType, mesLen, mesBody):
                    return False
        return True

    def onCommand(self, command: Constants.MessageType, lenOfData: int, data: bytes) -> bool:
        self.logger.info("processing command[{}], len[{}], data[{}]".format(command,lenOfData, data))
        if command.value == 1:
            self.clientName = data
            self.clients[self.clientName] = self
            self.statusUpdate(self.clientName, Constants.ClientStatus.ONLINE.value)
        elif command.value == 3:
            messageBody = data
            self.logger.info("user [{}] says [{}]".format(self.clientName, data))
            for processor in self.clients.values():
                processor.sendMessage(self.clientName, messageBody)
        elif command.value == 4:
            toClient, ignored, messageBody = data.partition(b':')
            messageBody = messageBody
            self.logger.info("from [{}] to [{}] message [{}]".format(self.clientName, toClient, messageBody))
            if toClient in self.clients:
                if self.clients[toClient] != None:
                    self.clients[toClient].sendMessageToClient(self.clientName, messageBody)
                else:
                    toClient = toClient.decode('UTF-8')
                    self.logger.info("client {} left our server and we can't send message to him".format(toClient))
            else:
                self.logger.info("no client [{}] on server".format(toClient))
        elif command.value == 2:
            messageBody = data
            for processor in self.clients.values():
                processor.sendPicToClient(self.clientName, messageBody)
        elif command.value == 5:
            del self.clients[self.clientName]
            return False
        else:
            self.logger.info('no such command')
            return False
        return True

    def statusUpdate(self, fromClient, newStatus: Constants):
        if newStatus == 1:
            byteStatus = b'1'
        else:
            byteStatus = b'2'
        for processor in self.clients.values():
            if processor != None:
                processor.sendStatusToClient(fromClient, byteStatus)

    def sendStatusToClient(self, fromClient: bytes, status: bytes):
        if self.clientName != fromClient:
            forSend =bytearray(b'6'+ fromClient + status)
            self.conn.sendall(forSend)

    def sendMessageToClient(self, fromClient: bytes, message: bytes):
        if self.clientName != fromClient:
            self.conn.sendall(b'4' + fromClient + message)

    def sendMessage(self, fromClient: bytes, message: bytes):
        if self.clientName != fromClient:
            self.conn.sendall(b'3' + fromClient + message )

    def sendPicToClient(self, fromClient: bytes, pic: bytes):
        if self.clientName != fromClient:
            self.conn.sendall(b'2' + fromClient + pic)


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
