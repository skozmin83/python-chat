#!/usr/bin/env python3
import socket
import Logging
import ClientStatus
from threading import Thread


class SingleClientCommandProcessor:
    logger = Logging.getLogger("processor")

    def __init__(self, clients: dict, conn: socket, ip, port):
        self.conn = conn
        self.clients = clients
        self.ip = ip
        self.port = port
        self.clientName = None
        self.buffer = b''

    def start(self):
        self.logger.info("start processing commands")
        clientsMsg = b'clients:'
        for client in self.clients.keys():
            if client == str:
                clientsMsg += bytes(client,'UTF-8') + b' '
            else:
                clientsMsg += client + b' '
        clientsMsg += b";"
        self.conn.sendall(clientsMsg)

    def finish(self):
        self.logger.info("finish processing commands")
        for processor in self.clients.values():
            processor.statusUpdate(self.clientName, ClientStatus.ClientStatus.OFFLINE)
        self.clients[self.clientName] = None

    def processNewChunk(self, chunk: bytes) -> bool:
        self.buffer += chunk
        while True:
            if b';' not in self.buffer:
                break
            message, ignored, self.buffer = self.buffer.partition(b';')
            messageType, ignored, messageBody = message.partition(b':')
            if not self.onCommand(messageType, messageBody):
                return False
        return True

    def onCommand(self, command: bytes, data: bytes) -> bool:
        self.logger.info("processing command[{}], data[{}]".format(command, data))
        if command == b'name':
            self.clientName = data
            self.clients[self.clientName] = self
            for processor in self.clients.values():
                processor.statusUpdate(self.clientName, ClientStatus.ClientStatus.ONLINE)
        elif command == b'msg':
            messageBody = data
            self.logger.info("user [{}] says [{}]".format(self.clientName, data))
            for processor in self.clients.values():
                processor.sendMessageToClient(self.clientName, messageBody)
        elif command == b'msg-to-client':
            toClient, ignored, messageBody = data.partition(b':')
            self.logger.info("from [{}] to [{}] message [{}]".format(self.clientName, toClient, messageBody))
            if toClient in self.clients:
                self.clients[toClient].sendMessageToClient(self.clientName, messageBody)
            else:
                self.logger.info("no client [{}] on server".format(toClient))
        elif command == b'exit':
            return False
        return True

    def statusUpdate(self, clientName: bytes, newStatus: ClientStatus.ClientStatus):
        if clientName != bytes(self.clientName):
            self.conn.sendall(b'status-update:' + clientName + bytes(newStatus.name, "UTF-8") +b';')

    def sendMessageToClient(self, fromClient: bytes, message: bytes):
        if self.clientName != fromClient:
            self.conn.sendall(b'msg:' + fromClient + b":" + b' ' + message+ b';')


class ClientThread(Thread):
    logger = Logging.getLogger("clientThread")

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
            self.logger.info("unknown error", exc_info=True)
        finally:
            self.logger.info("exiting thread")
            self.processor.finish()


BUFFER_SIZE = 1024

HOST = '127.0.0.1'
PORT = 12346

mainLogger = Logging.getLogger("main")

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
