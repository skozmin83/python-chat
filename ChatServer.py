#!/usr/bin/env python3
import socket
import Logging
from threading import Thread                                                       # импортируем Thread которая позволит создавать разные потоки, если это не запускать, то приложения получаются однопоточные


class CommandProcessor:                                                            # создан тип Command Processor
    logger = Logging.getLogger("processor")

    def __init__(self, clients: map, conn:socket, ip, port):                       # задаем параметры класса
        self.conn = conn
        self.clients = clients
        self.ip = ip
        self.port = port
        self.clientName = None
        self.buffer = b''

    def start(self):                                                               # этот метод запускает инфо логера
        self.logger.info("start processing commands")
        self.clientsOnline(self.clients, self.clientName)

    def clientsOnline(self, allClients: dict, clientName:bytes):
        clients = ''
        for key in allClients.keys():
            clients+=str(key,'UTF-8')+' '
        clients = bytes(clients, 'UTF-8')
        self.conn.sendall(b'these clients are online now: ' + clients)

    def finish(self):                                                              # эта функция запускает инфо логера и задает значение в словаре clients по ключу clientName = None
        self.logger.info("finish processing commands")
        self.clients[self.clientName] = None

    def processNewChunk(self, chunk:bytes) -> bool:                                      # этот метод принимает новый кусок данных
        self.buffer += chunk                                                       # добавляет их к данным буфера
        while True:
            if b';' not in self.buffer:                                            # если байтов ; нет в буфере, выход из цикла
                break
            message, ignored, self.buffer = self.buffer.partition(b';')            # разделяет содержимое в буфере на части и присваивает их значения картежу, если находит разделитель ";"
            messageType, ignored, messageBody = message.partition(b':')            # разделяет содержимое в сообщении на части и присваивает их значения картежу, если находит разделитель ":"
            if not self.onCommand(messageType, messageBody):                               # запускает функцию OnCommand и передает в нее аргументами тип сообщения и тело сообщения
                return False
        return True

    def onCommand(self, command:bytes, data:bytes) -> bool:
        self.logger.info("processing command[{}], data[{}]".format(command, data)) # запускает инфо логера который распечатывает какие аргументы были переданы в функцию
        if command == b'name':                                                     # если значение байтов = 'name'
            self.clientName = data
            # присваивает clientName = переводу в строку параметра data
            self.clients[self.clientName] = self # создает новый ключ в словаре clients  равный clientName
        elif command == b'msg':                                                    # если в байтах сообщение
            self.logger.info("user [{}] says [{}]".format(self.clientName, data))  # запускается инфологер с содержанием имени клиента и сообщения
        elif command == b'msg-to-client':
            toClient, ignored, messageBody = data.partition(b':')
            self.logger.info("from [{}] to [{}] message [{}]".format(self.clientName, toClient, messageBody))
            if toClient in self.clients:
                self.clients[toClient].sendMessageToClient(self.clientName, messageBody)
            else:
                self.logger.info("no client [{}] on server".format(toClient))
        elif command == b'exit':
            return False
        return True                                                                # всегда возвращает True

    def sendMessageToClient(self, fromClient:bytes, message:bytes):
        self.conn.sendall(b'msg:' + fromClient + b":" + message + b';')

                                                                                   # Multithreaded Python server : TCP Server
class ClientThread(Thread):                                                        # создан новый тип ClientThread принимающий параметр Thread
    logger = Logging.getLogger("clientThread")                                     # создает логера 'ClientThread'

    def __init__(self, processor: CommandProcessor, conn: socket):
        Thread.__init__(self, name="t-{}:{}".format(ip, port), daemon=True )       # инициируется новый поток, задается его имя, daemon означает что поток будет завершен сразу после выхода из программы
        self.processor = processor
        self.conn = conn

    def run(self):                                                                 # если запустить напрямую то будет выполнятся в том же потоке что и основной код
        try:
            self.processor.start()                                                 #запускает метод start у объекта типа CommandProcessor, который запустит инфо логера и выведет сообщение о начале обработки команд
            with self.conn:                                                        # с переданным сокетом
                while True:
                    data = self.conn.recv(1024)                                    # в бесконечном цикле принимаем по 1кб данных от клиента
                    if not data:                                                   # если данных нет, ничего не возвращает
                        return
                    if not self.processor.processNewChunk(data):                   # если нет новых данных, ничего не возвращает
                        return
        except ConnectionResetError:                                               # вместо ошибки сброса соединения запускает инфо логера
            self.logger.info("client closed connection")
        except:                                                                    # вместо остальных ошибок запускает инфо логера + показывает информацию об ошибке
            self.logger.info("unknown error", exc_info=True)
        finally:                                                                   # в концезапускает инфо логера выходим из нити и запускает метод finish у объекта типа CommandProcessor
            self.logger.info("exiting thread")
            self.processor.finish()                                                # метод finish запустит инфо логера и обнулит значение по ключу ClientName


BUFFER_SIZE = 1024                                                                 # Usually 1024, but we need quick response

HOST = '127.0.0.1'                                                                 # Standard loopback interface address (localhost)
PORT = 12346
# Port to listen on (non-privileged ports are > 1023)

mainLogger = Logging.getLogger("main")

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((HOST, PORT))
threads = []
allClients = {}

mainLogger.info("SERVER: Waiting for connections from TCP clients on {}:{} ...".format(HOST, PORT))
while True:
    tcpServer.listen()                                                             # у tcp Server'a запускается режим прослушивания с неограниченным количеством подключений
    (connection, (ip, port)) = tcpServer.accept()                                  # задано имя нового сокета и адрес клиента
    processor = CommandProcessor(allClients, connection, ip, port)                 # создается новый объект типа CommandProcessor
    newthread = ClientThread(processor, connection)                                # создается новый объект типа ClientThread
    newthread.start()                                                              # запускается объект класса ClientThread который после запуска вызовет содержание функции run() в отдельном потоке
    threads.append(newthread)                                                      # в список добавляется объект класса ClientThread

for t in threads:
    t.join()                                                                       # соединяет все элементы в массиве threads

mainLogger.info("SERVER: Exit")                                                    # запусается главный инфо логер

# main ---------|------------------------------------
#                t-127.128.1.1-----------------------