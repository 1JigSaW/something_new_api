import httpx
from uuid import uuid4
from app.main import create_app


async def test_replacement_limit_free() -> None:
    app = create_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        email = f"limit-{uuid4().hex[:8]}@example.com"
        r1 = await client.post("/api/auth/request-code", json={"email": email})
        assert r1.status_code == 204
        token = (await client.post("/api/auth/verify", json={"email": email, "code": email.split("@")[0]})).json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        ok = await client.post("/api/replacements/", json={"from_item": "coffee", "to_item": "water"}, headers=headers)
        assert ok.status_code == 201
        limit = await client.post("/api/replacements/", json={"from_item": "soda", "to_item": "tea"}, headers=headers)
        assert limit.status_code == 429


