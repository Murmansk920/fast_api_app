import pytest_asyncio
from httpx2 import ASGITransport, AsyncClient
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from db import async_get_db
from main import app
from models.base import Base          # SQLAlchemy 模型基类

# 1. 造一个独立的测试数据库（内存 SQLite，速度快、不残留）
TEST_DB_URL = "sqlite:///:memory:"

# 测试数据库引擎
engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    poolclass=StaticPool,
)

@pytest_asyncio.fixture(scope="function")
async def db_session():
    # ==========================================
    # 🌟 核心建表逻辑：用异步连接跑同步的 create_all
    # ==========================================
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)# type: ignore

    # 创建会话
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session

    # ==========================================
    # 🌟 核心删表逻辑：测试结束后销毁所有表
    # ==========================================
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)# type: ignore

@pytest_asyncio.fixture
async def client(db_session):  # ← 这里通过参数获取 db_session 的实例
    # 定义一个标准的异步生成器，作为依赖
    async def override_get_db():
        yield db_session  # ← 返回实际的 session 对象，而不是 fixture 函数

    # 在 fixture 内部覆盖依赖
    app.dependency_overrides[async_get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    # 测试结束后清除覆盖（好习惯）
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def auth_headers(client):
    # 注意这里也要 await
    await client.post("/users/register", json={"username": "tester", "password": "123456", "email": "tester@qq.com"})
    resp = await client.post("/auth/login", data={"username": "tester", "password": "123456","email": "tester@qq.com"})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

