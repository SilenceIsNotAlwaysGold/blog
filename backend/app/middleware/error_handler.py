"""
Global exception handler middleware
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.utils.response import error
import traceback


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content=error(
            message=exc.detail,
            code=exc.status_code
        )
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    errors = []
    for error_detail in exc.errors():
        field = " -> ".join(str(loc) for loc in error_detail["loc"])
        message = error_detail["msg"]
        errors.append(f"{field}: {message}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error(
            message="Validation error",
            code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details="; ".join(errors)
        )
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    # Log the exception
    print(f"Unhandled exception: {exc}")
    print(traceback.format_exc())

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error(
            message="Internal server error",
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=str(exc) if request.app.debug else None
        )
    )


def register_exception_handlers(app):
    """Register all exception handlers to the FastAPI app"""
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
