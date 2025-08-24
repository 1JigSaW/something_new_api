import httpx
from app.main import create_app


async def test_read_me_creates_user_if_missing() -> None:
    app = create_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/users/me", headers={"X-User-Email": "me@example.com"})
        assert response.status_code == 200
        body = response.json()
        assert body["email"] == "me@example.com"
        assert body["is_active"] is True


