from typing import Annotated

import jwt
from datetime import datetime, timezone
from fastapi import Depends, HTTPException, Header, status

from app.core.settings import get_settings
from app.core.security import is_token_blacklisted


def get_current_user_id(
    authorization: Annotated[str | None, Header(alias="Authorization")] = None,
) -> int:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = authorization.split(" ", 1)[1]
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        if is_token_blacklisted(jti=str(payload.get("iat"))):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        sub = payload.get("sub")
        return int(sub)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


