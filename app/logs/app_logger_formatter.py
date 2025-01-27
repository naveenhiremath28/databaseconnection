import logging, json
from logging import StreamHandler
from logging.handlers  import RotatingFileHandler
from fastapi import Request, Response
from http import HTTPStatus
from app.logs.app_logger import get_logging
import uuid
import os
from app.logs.app_logger import FILE_NAME
from fastapi.responses import JSONResponse
from app.exceptions.app_exceptions import CredentialsException
from app.kafka.producer import produce

class JsonStreamHandler(StreamHandler):

    def emit(self, record):
        log_entry = json.loads(self.format(record))
        topic = "connections"
        produce(topic=topic, log_entry=log_entry)

class JSONFileHandler(RotatingFileHandler):

    def __init__(self, formatter, filename, maxBytes, backupCount):
        super().__init__(filename, maxBytes, backupCount)
        self.setFormatter(formatter)

    def emit(self, record):
        log_entry = json.loads(self.format(record))
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "a+") as file:
                file.seek(0)
                try:
                    logs = json.load(file)
                except Exception:
                    logs = []
                file.truncate(0)
                logs.append(log_entry)
                json.dump(logs, file, indent=2)
        else:
            with open(FILE_NAME, "w") as file:
                json.dump([log_entry], file, indent=2)


class JSONFormatter(logging.Formatter):
    def __init__(self, fmt):
        logging.Formatter.__init__(self, fmt)
    
    def format(self, record):
        logging.Formatter.format(self, record)
        return json.dumps(get_log(record), indent=2)

def get_log(record):
    data = {
        "time": record.asctime,
        "id": str(uuid.uuid4()),
        "process_name": record.name,
        "level": record.levelname,
        "pathname": record.pathname,
        "message": record.message
    }

    if hasattr(record, "extra_info"):
        data["req"] = record.extra_info["req"]
        data["res"] = record.extra_info["res"]

    return data

def get_extra_info(request: Request, response: Response, process_time):
    return {
        "req": {
            "url": request.url.path,
            "headers": {
                "host": request.headers["host"],
                "user_agent": request.headers["user-agent"],
                "accept": request.headers["accept"]
            },
            "method": request.method,
            "http_version": request.scope["http_version"],
        },
        "res": {
            "status_code": response.status_code,
            "status": HTTPStatus(response.status_code).phrase,
            "res_time": process_time
        }
    }


def write_log_data(request, response, process_time):
    logger.info(
        request.method + " " + request.url.path,
        extra={"extra_info": get_extra_info(request, response, process_time)}
    )

formatter = JSONFormatter("%(asctime)s")
logger = get_logging(__name__,formatter)

def response_message(e: CredentialsException):
    logger.info("No Token")
    return JSONResponse({"detail": e.detail}, status_code=e.status_code)
