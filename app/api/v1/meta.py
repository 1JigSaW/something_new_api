from fastapi import APIRouter


router = APIRouter(prefix="/meta", tags=["meta"])


@router.get("/filters")
async def meta_filters():
    return {
        "categories": ["movement", "breath", "mindset", "nutrition"],
        "sizes": ["small", "medium", "large"],
        "tags": ["walk", "mindful", "relax", "hydrate"],
    }


