from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker, Session

from config import settings

# 1. 引擎：连接池 + 数据库方言（开发期用 SQLite，零安装）
engine = create_engine(
    "sqlite:///./data/app.db",
    echo=True,          # 打印每条 SQL，调试期开着
    connect_args={"check_same_thread": False},  # SQLite 必需
)

# 2. 会话工厂：每个请求来一个 Session，用完即还
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# def get_db():                 # 3. FastAPI 依赖：yield 管理生命周期
#     db: Session = SessionLocal()
#     try:
#         yield db               # 路由函数拿到的就是这个 db
#     finally:
#         db.close()             # 无论成功还是抛异常，连接一定归还

async_engine = create_async_engine(settings.database_url, echo=True)
AsyncSessionLocal = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

async def async_get_db():
    async with AsyncSessionLocal() as db:   # 退出时自动 close
        yield db