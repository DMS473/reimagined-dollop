from fastapi.responses import JSONResponse
from typing import Any

def success_response(data: Any, message: str = "Operation successful", status_code: int = 200) -> JSONResponse:
    return JSONResponse(
        content={
            "status": status_code,
            "success": True,
            "message": message,
            "data": data
        }
    )

def error_response(message: str = "An error occurred", status_code: int = 400) -> JSONResponse:
    return JSONResponse(
        content={
            "status": status_code,
            "success": False,
            "message": message,
            "data": None
        }
    )