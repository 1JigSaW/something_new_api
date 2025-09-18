from fastapi import APIRouter
from app.api.v1 import auth as auth_v1
from app.api.v1 import challenges as challenges_v1
from app.api.v1 import users as users_v1
from app.api.v1 import replacements as replacements_v1
from app.api.v1 import profile as profile_v1
from app.api.v1 import meta as meta_v1
from app.api.v1 import admin as admin_v1
from app.api.v1 import activity as activity_v1


api_router = APIRouter()
api_router.include_router(users_v1.router)
api_router.include_router(auth_v1.router)
api_router.include_router(challenges_v1.router)
api_router.include_router(replacements_v1.router)
api_router.include_router(profile_v1.router)
api_router.include_router(activity_v1.router)
api_router.include_router(meta_v1.router)
api_router.include_router(admin_v1.router)


