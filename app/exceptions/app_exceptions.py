from fastapi import HTTPException
from typing import Any

class APIResponseException(HTTPException):
    def __init__(self, status_code: int, detail: Any):
        super().__init__(status_code=status_code, detail=detail)