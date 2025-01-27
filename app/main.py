import uvicorn
from fastapi import FastAPI
from app.routes.db_routes import db_router
from app.jwt_handler.auth import get_current_active_user
from app.exceptions.app_exceptions import CredentialsException
from app.logs.app_logger_formatter import logger, Request, write_log_data, response_message
import time

app = FastAPI()

app.include_router(db_router)


@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = time.time()
    if request.url.path.startswith("/connection/"):
        try:
            if get_current_active_user():
                response = await call_next(request)
                end_time = time.time()
                process_time = end_time - start_time
                write_log_data(request, response, process_time)
                return response
        except CredentialsException as e:
            return response_message(e)
    else:
        response = await call_next(request)
        end_time = time.time()
        process_time = end_time - start_time
        write_log_data(request, response, process_time)
        return response

if __name__ == "__main__":
    logger.info("Server is ALIVE !!!")
    uvicorn.run(app, host="127.0.0.1", port=8000)
