from redis import Redis
from rq import Queue

from app.core.settings import get_settings


def get_redis_connection() -> Redis:
    settings = get_settings()
    return Redis.from_url(
        url=settings.redis_url,
    )


def get_queue(
    name: str | None = None,
) -> Queue:
    settings = get_settings()
    queue_name = name or settings.rq_default_queue_name
    return Queue(
        name=queue_name,
        connection=get_redis_connection(),
    )


