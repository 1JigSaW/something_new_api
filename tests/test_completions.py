import httpx
from uuid import uuid4
from app.main import create_app
from app.tasks.seed_challenges import seed as seed_challenges


async def test_challenge_completion_and_day_pass() -> None:
    app = create_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        email = f"done-{uuid4().hex[:8]}@example.com"
        assert (await client.post("/api/auth/request-code", json={"email": email})).status_code == 204
        token = (await client.post("/api/auth/verify", json={"email": email, "code": email.split("@")[0]})).json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        # Seed challenges and pick first id
        await seed_challenges()
        lst = await client.get("/api/challenges/")
        cid = lst.json()[0]["id"]
        r = await client.post(f"/api/challenges/{cid}/complete", headers=headers)
        assert r.status_code == 201
        r2 = await client.post(f"/api/challenges/{cid}/complete", headers=headers)
        assert r2.status_code == 429
        # Day profile should show passed
        prof = await client.get("/api/profile/day", headers=headers)
        assert prof.status_code == 200
        body = prof.json()
        assert body["day_passed"] is True


