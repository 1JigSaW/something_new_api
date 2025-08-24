import httpx
from uuid import uuid4
from app.main import create_app


async def test_auth_flow() -> None:
    app = create_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        email = f"user-{uuid4().hex[:8]}@example.com"
        resp = await client.post("/api/auth/request-code", json={"email": email})
        assert resp.status_code == 204
        code = email.split("@")[0]
        resp2 = await client.post("/api/auth/verify", json={"email": email, "code": code})
        assert resp2.status_code == 200
        body = resp2.json()
        assert body["token_type"] == "bearer"
        assert isinstance(body["access_token"], str)
        token = body["access_token"]
        me = await client.get("/api/users/me-auth", headers={"Authorization": f"Bearer {token}"})
        assert me.status_code == 200


async def test_request_code_rate_limit() -> None:
    app = create_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        email = f"rate-{uuid4().hex[:8]}@example.com"
        r1 = await client.post("/api/auth/request-code", json={"email": email})
        assert r1.status_code == 204
        r2 = await client.post("/api/auth/request-code", json={"email": email})
        assert r2.status_code == 429


