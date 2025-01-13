from fastapi.responses import JSONResponse
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from app.routes.db_routes import db_router
import time
import asyncio
from jwt.exceptions import InvalidTokenError
from app.jwt_handler.auth import get_current_active_user
from app.exceptions.app_exceptions import CredentialsException

app = FastAPI()

app.include_router(db_router)

@app.middleware("http")
async def process_time(request: Request, call_next):
    if request.url.path.startswith("/connection/"):
        try:
            if get_current_active_user():
                response = await call_next(request)
                return response
        except CredentialsException as e:
            return JSONResponse({"detail": e.detail}, status_code=e.status_code)
    else:
        response = await call_next(request)
        return response


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)