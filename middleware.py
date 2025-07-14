from fastapi_throttling  import ThrottlingMiddleware
from fastapi import FastAPI, Request, Response, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import time
LIMIT=10
PERIOD=60  # seconds
# ALLOWED_CONTENT_TYPES = ["image/jpeg", "image/png"]

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def __init__(self, limit: int, period:int):
        self.limit =  LIMIT
        self.period = PERIOD
        self.request_count = {}
 

    async def dispatch(self, request: Request, call_next):
        request_count = getattr(self, 'request_count', {})
        client_ip = request.client.host if request.client else "unknown"
        if client_ip not in request_count:
            request_count[client_ip] = []
        request_number = request_count[client_ip]
        #current_time = request.scope.get("time", 0)
        current_time = time.time()
        # Clean up old requests
        request_count[client_ip] = [t for t in request_number if t > current_time - self.period]
        if len(request_count[client_ip]) >= self.limit:
            return Response(
                content='{"detail":"Rate limit exceeded"}',
                status_code=429,
                media_type="application/json"
            )
        response = await call_next(request)
        return response
        
# class FileTypeLimitMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         # Only check for file upload endpoints
#         if request.url.path.startswith("/upload_basic_file"):
#             content_type = request.headers.get("content-type", "")
#             # For multipart/form-data, content_type will include boundary, so check startswith
#             if not any(content_type.startswith(allowed) for allowed in ALLOWED_CONTENT_TYPES):
#                 raise HTTPException(
#                     status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
#                     detail="File type not allowed. Only JPEG and PNG are accepted."
#                 )
#         response = await call_next(request)
#         return response