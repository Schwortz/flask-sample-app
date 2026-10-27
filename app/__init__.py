import logging
import os
import platform
from logging.handlers import RotatingFileHandler

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(redirect_slashes=False)

log_dir = os.path.join(os.path.expanduser("~"), ".flask_sample_app")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "flask_sample_app.log")

file_handler = RotatingFileHandler(log_file, maxBytes=1_048_576, backupCount=5)
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s %(levelname)s [%(name)s] %(message)s"
))
file_handler.setLevel(logging.INFO)

logger = logging.getLogger("flask_sample_app")
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

logger.info(
    "Application starting — host=%s, platform=%s, log_file=%s",
    platform.node(), platform.system(), log_file,
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse({"error": str(exc.detail)}, status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Flask never matched a non-int id, so a bad path param is a plain 404.
    if any(err["loc"] and err["loc"][0] == "path" for err in exc.errors()):
        return JSONResponse({"error": "Not Found"}, status_code=404)
    return JSONResponse({"error": "Invalid request body"}, status_code=422)


from app.routes import router  # noqa: E402

app.include_router(router)
