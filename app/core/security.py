from datetime import datetime, timedelta, timezone
import jwt
import redis

from app.core.settings import get_settings


def create_access_token(
    subject: str,
) -> str:
    settings = get_settings()
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=settings.jwt_access_ttl_minutes)
    payload = {"sub": subject, "iat": int(now.timestamp()), "exp": int(exp.timestamp())}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def create_refresh_token(
    subject: str,
) -> str:
    settings = get_settings()
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=settings.jwt_refresh_ttl_minutes)
    payload = {"sub": subject, "iat": int(now.timestamp()), "exp": int(exp.timestamp())}
    return jwt.encode(payload, settings.jwt_refresh_secret, algorithm=settings.jwt_algorithm)


def is_token_blacklisted(
    jti: str,
) -> bool:
    settings = get_settings()
    try:
        r = redis.from_url(settings.redis_url)
        return r.exists(f"{settings.jwt_blacklist_prefix}{jti}") == 1
    except Exception:
        # If Redis is unavailable, treat as not blacklisted to avoid 500
        return False


def blacklist_token(
    jti: str,
    ttl_seconds: int,
) -> None:
    settings = get_settings()
    try:
        r = redis.from_url(settings.redis_url)
        r.setex(name=f"{settings.jwt_blacklist_prefix}{jti}", time=ttl_seconds, value=1)
    except Exception:
        # If Redis is unavailable, skip blacklisting silently in development/local
        return


