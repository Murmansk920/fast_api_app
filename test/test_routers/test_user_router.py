import pytest

@pytest.mark.asyncio
async def test_create_user_validation_error(client):
    # 缺少 email 字段 -> 422
    resp = await client.post("/users/register", json={"username": "Bob"})
    assert resp.status_code == 422


# ---------- GET /users/ ----------
@pytest.mark.asyncio
async def test_list_users_success(client,auth_headers):
    user_out1 = {"id": 1,"username": "tester"}
    await client.post("/users/register", json={"username": "tester", "password": "123456", "email": "tester@qq.com"})
    resp = await client.get("/users/",headers=auth_headers)
    assert resp.json() == [user_out1]
    await client.post("/users/register", json={"username": "tester2", "password": "123456", "email": "tester@qq.com"})
    resp = await client.get("/users/",headers=auth_headers)
    user_out2 = [{"id": 1,"username": "tester"},{"id": 2,"username": "tester2"}]
    assert resp.status_code == 200
    assert resp.json() == user_out2


# ---------- PUT /users/user/{user_id} ----------
@pytest.mark.asyncio
async def test_modify_user_success(client):
    await client.post("/users/register", json={"username": "tester", "password": "123456", "email": "tester@qq.com"})
    resp = await client.put("/users/user/1", json={"password": "123456"})
    assert resp.status_code == 200
    resp = await client.get("/users/1")
    assert resp.json() == {"id": 1,"username": "tester"}


@pytest.mark.asyncio
async def test_modify_user_invalid_id(client):
    resp = await client.put("/users/user/abc", json={"password": "123456"})
    assert resp.status_code == 422


# ---------- GET /users/{user_id} ----------
@pytest.mark.asyncio
async def test_get_user_success(client):
    await client.post("/users/register", json={"username": "tester", "password": "123456", "email": "tester@qq.com"})
    resp = await client.get("/users/1")
    assert resp.status_code == 200
    assert resp.json() == {"id": 1,"username": "tester"}

@pytest.mark.asyncio
async def test_get_user_not_found(client):
    await client.post("/users/register", json={"username": "tester", "password": "123456", "email": "tester@qq.com"})
    resp = await client.get("/users/999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "用户不存在"


# ---------- DELETE /users/{user_id} ----------
@pytest.mark.asyncio
async def test_delete_user_success(client):
    await client.post("/users/register", json={"username": "tester", "password": "123456", "email": "tester@qq.com"})
    resp = await client.delete("/users/1")
    assert resp.status_code == 204
    assert resp.content == b""

@pytest.mark.asyncio
async def test_delete_user_not_found(client):
    await client.post("/users/register", json={"username": "tester", "password": "123456", "email": "tester@qq.com"})
    resp = await client.delete("/users/999")
    assert resp.status_code == 404