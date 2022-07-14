
from typing import NoReturn, Optional, Dict, Type, Generator
from fastapi import status, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
DEFAULT_ERROR_MESSAGE = "error occurred check the request"

def _raise_api_error(
    detail: Optional[str], status_code: int, headers: Optional[Dict[str, str]] = None, exc: Optional[Exception] = None,
    debug: bool = False
) -> NoReturn:
    if debug and exc is not None:
        detail = str(exc)
    if detail is None:
        detail = DEFAULT_ERROR_MESSAGE
    raise HTTPException(detail=detail, status_code=status_code, headers=headers)


def raise_api_exception(status_code: int = HTTP_400_BAD_REQUEST, 
                        detail: Optional[str]=DEFAULT_ERROR_MESSAGE,
                        exc: Optional[Exception] = None ) -> NoReturn:
    debug = False
    if exc is not None:     
        debug = True
        detail = str(exc)
    _raise_api_error(debug=debug, detail=detail, status_code=status_code, exc=exc)