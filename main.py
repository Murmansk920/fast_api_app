from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from config import settings
from db import engine
from dependencies.utils import limiter
from exceptions import rate_limit_handler, global_handler
from models.users import Base
from routers.users import router as users_router  # 导入子路由
from routers.auth import router as auth_router
from routers.tasks import router as tasks_router

Base.metadata.create_all(bind=engine)   # 启动时建表

app = FastAPI(title=settings.app_name, debug=settings.debug)
app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, rate_limit_handler)
app.add_exception_handler(Exception, global_handler)

# 汇总：这一步不写，users.py 里的接口对外完全不可见！
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(tasks_router)