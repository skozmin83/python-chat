#!/usr/bin/env python3
import socket
import Logging
from threading import Thread


class CommandProcessor:
    logger = Logging.getLogger("processor")

    def __init__(self, clients: map, conn:socket, ip, port):
        self.conn = conn
        self.clients = clients
        self.ip = ip
        self.port = port
        self.clientName = None
        self.buffer = b''
        # self.logger = Logging.getLogger("processor")

    def start(self):
        self.logger.info("start processing commands")

    def finish(self):
        self.logger.info("finish processing commands")
        self.clients[self.clientName] = None

    def processNewChunk(self, chunk):
        self.buffer += chunk
        while True:
            if b';' not in self.buffer:
                break
            message, ignored, self.buffer = self.buffer.partition(b';')
            messageType, ignored, messageBody = message.partition(b':')
            self.onCommand(messageType, messageBody)

    def onCommand(self, command, data) -> bool:
        self.logger.info("processing command[{}], data[{}]".format(command, data))
        if command == b'name':
            self.clientName = str(data)
            self.clients[self.clientName] = self
        elif command == b'msg':
            self.logger.info("user [{}] says [{}]".format(self.clientName, data))
        return True


# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread):
    logger = Logging.getLogger("clientThread")

    def __init__(self, processor: CommandProcessor, conn: socket):
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


# Multithreaded Python server : TCP Server Socket Program Stub
BUFFER_SIZE = 1024  # Usually 1024, but we need quick response

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 12346  # Port to listen on (non-privileged ports are > 1023)

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
    processor = CommandProcessor(allClients, connection, ip, port)
    newthread = ClientThread(processor, connection)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()

mainLogger.info("SERVER: Exit")
