import httpx
from app.tasks.seed_challenges import seed as seed_challenges
from app.main import create_app


async def test_challenges_list_and_get() -> None:
    app = create_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        await seed_challenges()
        resp = await client.get("/api/challenges/?free_only=true")
        assert resp.status_code == 200
        items = resp.json()
        assert isinstance(items, list)


