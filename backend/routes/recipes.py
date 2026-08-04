from fastapi import APIRouter, HTTPException
from backend.api_models import RecipeResponse, RecipeRequest


recipes_router = APIRouter(prefix="/recipes", tags=["recipes"])

@recipes_router.get("/")
async def get_recipes(response_model=list[RecipeResponse]) -> list[RecipeResponse]:
    pass
