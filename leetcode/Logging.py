import logging
import sys
from logging.handlers import TimedRotatingFileHandler

# for more info look here: https://www.toptal.com/python/in-depth-python-logging

# FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
FORMATTER = logging.Formatter(
    "%(asctime)-15s [%(levelname)-5s][%(threadName)-20s][%(filename)s:%(lineno)d] %(message)s")
CHAT_FORMATTER = logging.Formatter("%(asctime)-15s %(message)s")

def getConsoleHandler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CHAT_FORMATTER)
    return console_handler


def getFileHandler(file_name:str):
    file_handler = TimedRotatingFileHandler(file_name, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def getConsoleLogger(logger_name=""):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    # better to have too much log than not enough
    logger.addHandler(getConsoleHandler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger

def getChatLogger(logger_name="", file_name="./chat6.log"):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    # better to have too much log than not enough
    logger.addHandler(getConsoleHandler())
    logger.addHandler(getFileHandler(file_name))
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger


def getLogger(logger_name="", file_name="./chat6.log"):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    # better to have too much log than not enough
    # logger.addHandler(getConsoleHandler())
    logger.addHandler(getFileHandler(file_name))
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger
