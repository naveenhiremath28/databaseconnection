import sys
import logging
from logging.handlers import RotatingFileHandler

FILE_NAME = "fastapi_logs.json"


def get_file_handler(formatter, filename=FILE_NAME,maxBytes=1024*1024, backupCount=3):
    from app.logs.app_logger_formatter import JSONFileHandler
    file_handler = JSONFileHandler(formatter, filename, maxBytes, backupCount)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    return file_handler

def get_stream_handler_file(formatter):
    from app.logs.app_logger_formatter import JsonStreamHandler
    stream_handler = JsonStreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    return stream_handler

def get_stream_handler(formatter):
    from logging import StreamHandler
    stream_handler = StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    return stream_handler

def get_logging(name, formatter):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_stream_handler_file(formatter))
    logger.addHandler(get_file_handler(formatter))
    logger.addHandler(get_stream_handler(formatter))
    return logger