import httpx
from app.main import create_app


async def test_healthcheck() -> None:
    app = create_app()
    transport = httpx.ASGITransport(
        app=app,
    )
    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.get(
            url="/health",
        )
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


