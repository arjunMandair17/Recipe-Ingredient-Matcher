from fastapi import APIRouter
from backend.api_models import IngredientResponse, IngredientRequest

ingredients_router = APIRouter(prefix="/ingredients", tags=["ingredients"])

@ingredients_router.get("/")
async def get_ingredients(ingredient_request: IngredientRequest) -> IngredientResponse:
    # return all ingredients from the database

    return IngredientResponse(
        id=1,
        name="Ingredient 1",
        price=10.0,
        price_url="https://www.google.com",
        quantity=1.0,
        unit="g"
    )