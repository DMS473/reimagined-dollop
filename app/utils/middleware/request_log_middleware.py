from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from aiologger import Logger
from aiologger.handlers.files import AsyncFileHandler
from aiologger.handlers.streams import AsyncStreamHandler
import logging
import time

# Create an asynchronous logger instance
requestLogger = Logger(name="request_logger")
requestLogger.level = logging.INFO  # Set the log level for the logger

# Create an async file handler
file_handler = AsyncFileHandler("app/log/request.log")  # Specify your log file

# Create a console handler
# console_handler = AsyncStreamHandler()

# Add the file handler to the logger
requestLogger.add_handler(file_handler)
# requestLogger.add_handler(console_handler)

# Create a formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Set the formatter to the logger (not the handler)
requestLogger.formatter = formatter

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log the incoming request
        start_time = time.time()
        requestLogger.info(f"Request: {request.method} {request.url}")
        requestLogger.info(f"Headers: {request.headers}")

        # Call the request and get the response
        response: Response = await call_next(request)

        # Log the outgoing response
        end_time = time.time()
        elapsed_time = end_time - start_time
        requestLogger.info(f"Response status: {response.status_code}")
        requestLogger.info(f"Time taken: {elapsed_time} seconds")
        requestLogger.info(f"Activity: {request.method} {request.url}\n")

        return response
