import pytest

@pytest.mark.asyncio
async def test_create_task(client, auth_headers):
    resp = await client.post("/tasks/", json={"title": "写周报","description":"1111"}, headers=auth_headers)
    assert resp.status_code == 201
    assert resp.json()["title"] == "写周报"

@pytest.mark.asyncio
async def test_get_tasks_requires_auth(client):
    resp = await client.get("/tasks/")
    assert resp.status_code == 401   # 没登录必须拦住

@pytest.mark.asyncio
async def test_get_tasks(client, auth_headers):
    await client.post("/tasks/", json={"title": "写周报", "description": "1111"}, headers=auth_headers)
    resp = await client.get("/tasks/", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()[0]["title"] == "写周报"

@pytest.mark.asyncio
async def test_update_task(client, auth_headers):
    await client.post("/tasks/", json={"title": "写周报", "description": "1111"}, headers=auth_headers)
    resp = await client.put("/tasks/1",json={"title":"写笔记","state":"todo"}, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["title"] == "写笔记"

@pytest.mark.asyncio
async def test_delete_not_found(client,auth_headers):
    resp = await client.delete("/tasks/9999", headers=auth_headers)
    assert resp.status_code == 404