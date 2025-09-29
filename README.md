## Something New API

### Overview
- Framework: FastAPI
- Entry points: `main.py` (uvicorn runner), `app/main.py` (app factory)
- Versioning: Routers are mounted at `/api` and `/api/v1` (same handlers)

### Router map
- `app/api/router.py` includes versioned routers under `app/api/v1/`:
  - `auth.py` → `/auth`
  - `users.py` → `/users`
  - `challenges.py` → `/challenges`
  - `replacements.py` → `/replacements`
  - `profile.py` → `/profile`
  - `activity.py` → `/activity`
  - `meta.py` → `/meta`
  - `admin.py` → `/admin`

All routes are reachable via `/api/...` and `/api/v1/...`.

### Key endpoints
- Auth
  - `POST /api/auth/request-code`
  - `POST /api/auth/verify`
  - `POST /api/auth/login`
  - `POST /api/auth/refresh`
  - `POST /api/auth/logout`
  - `GET  /api/auth/me`
- Users
  - `GET  /api/users/me`
  - `GET  /api/users/me-auth`
- Challenges
  - `GET  /api/challenges/`
  - `POST /api/challenges/{id}/complete`
- Profile
  - `GET  /api/profile/stats`

### App factory
- `create_app()` in `app/main.py` configures CORS, Sentry, logging, and mounts routers.

### Database
- SQLAlchemy async engine/session factory in `app/db/session.py`.
- Alembic migrations in `alembic/versions`.

### Conventions
- Add new API modules under `app/api/v1/` and include them in `app/api/router.py`.

