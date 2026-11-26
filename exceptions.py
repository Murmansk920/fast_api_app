from fastapi import Request
from fastapi.responses import JSONResponse

async def rate_limit_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=429, content={"error": "请求过于频繁"})

async def global_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": "服务器内部错误"})