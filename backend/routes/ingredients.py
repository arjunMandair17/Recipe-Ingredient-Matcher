from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from backend.api_models import IngredientResponse
from db.sql_init import get_session
from db.db_models import Ingredient, RecipeIngredient


ingredients_router = APIRouter(prefix="/ingredients", tags=["ingredients"])


@ingredients_router.get("/", response_model=list[IngredientResponse])
async def get_ingredients(recipe_id: int | None = None) -> list[IngredientResponse]:
    """Return all ingredients, or those linked to a recipe when recipe_id is set."""
    try:
        with get_session() as session:
            if recipe_id is not None:
                ingredients = session.scalars(
                    select(Ingredient)
                    .join(RecipeIngredient)
                    .where(RecipeIngredient.recipe_id == recipe_id)
                    .order_by(Ingredient.name)
                ).all()
                if not ingredients:
                    raise HTTPException(
                        status_code=404,
                        detail=f"No ingredients found for recipe ID: {recipe_id}",
                    )
            else:
                ingredients = session.scalars(
                    select(Ingredient).order_by(Ingredient.name)
                ).all()
                if not ingredients:
                    raise HTTPException(status_code=404, detail="No ingredients found")

            return [IngredientResponse.model_validate(row) for row in ingredients]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ingredients_router.get("/{ingredient_id}", response_model=IngredientResponse)
async def get_ingredient(ingredient_id: int) -> IngredientResponse:
    """Return a single ingredient by postgres id."""
    try:
        with get_session() as session:
            ingredient = session.scalars(
                select(Ingredient).where(Ingredient.id == ingredient_id)
            ).one_or_none()
            if not ingredient:
                raise HTTPException(status_code=404, detail="Ingredient not found")
            return IngredientResponse.model_validate(ingredient)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
