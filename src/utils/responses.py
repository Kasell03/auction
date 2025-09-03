from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi import status


def success_response(
        data: dict | list | None,
        status_code: int = status.HTTP_200_OK,
        message: str = "OK", **kwargs
) -> JSONResponse:

    return JSONResponse(status_code=status_code, content={
        "status": "success",
        "msg": message,
        "data": data,
        **kwargs,
    })

def error_exception(status_code: int, detail: str | list, **kwargs) -> HTTPException:
    return HTTPException(status_code=status_code, detail={"msg": detail, **kwargs})
