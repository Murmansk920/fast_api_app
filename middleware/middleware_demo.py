import time
from starlette.middleware.base import BaseHTTPMiddleware

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)   # 交给下一个处理者
        cost = time.time() - start
        response.headers["X-Process-Time"] = f"{cost:.3f}"  # 写入响应头
        print(f"{request.method} {request.url.path} "
              f"-> {response.status_code} ({cost:.3f}s)")
        return response

class TimingMiddleware2(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print("i am in TimingMiddleware2")
        response = await call_next(request)   # 交给下一个处理者
        print("leaving in TimingMiddleware2")
        return response

