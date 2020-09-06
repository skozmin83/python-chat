from enum import Enum

class ClientStatus(Enum):
    OFFLINE = 1
    ONLINE = 2

class MessageType(Enum):
    CLIENT_NAME = 1
    IMAGE = 2
    TEXT = 3
    TEXT_TO_CLIENT = 4
    EXIT = 5
    STATUS = 6
    CLIENTS_ONLINE = 7
    IMAGE_TO_CLIENT =8
    RECEIVER = 9