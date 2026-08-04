from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from backend.api_models import IngredientRequest, RecipeResponse
from db.sql_init import get_session
from db.db_models import Recipe, Ingredient, RecipeIngredient


recipes_router = APIRouter(prefix="/recipes", tags=["recipes"])


@recipes_router.get("/", response_model=list[RecipeResponse])
async def get_recipes() -> list[RecipeResponse]:
    """Return all recipes ordered by name."""
    try:
        with get_session() as session:
            recipes = session.scalars(select(Recipe).order_by(Recipe.name)).all()
            for recipe in recipes:
                recipe.ingredients = session.scalars(select(Ingredient).join(RecipeIngredient).where(RecipeIngredient.recipe_id == recipe.id)).all()
            if not recipes:
                raise HTTPException(status_code=404, detail="No recipes found")
            return [RecipeResponse.model_validate(recipe) for recipe in recipes]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting recipes: {str(e)}")


@recipes_router.get("/{recipe_id}", response_model=RecipeResponse)
async def get_recipe(recipe_id: int) -> RecipeResponse:
    """Return a single recipe by postgres id."""
    try:
        with get_session() as session:
            recipe = session.scalars(
                select(Recipe).where(Recipe.id == recipe_id)
            ).one_or_none()
            recipe.ingredients = session.scalars(select(Ingredient).join(RecipeIngredient).where(RecipeIngredient.recipe_id == recipe.id)).all()
            if not recipe:
                raise HTTPException(status_code=404, detail="Recipe not found")
            return RecipeResponse.model_validate(recipe)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting recipe: {str(e)}")


@recipes_router.post("/", response_model=list[RecipeResponse])
async def fetch_recipes_by_ingredients(ingredients: list[IngredientRequest]):
    """Fetch recipes by ingredients."""
    try:
        with get_session() as session:
            recipes = session.scalars(select(Recipe).join(RecipeIngredient).join(Ingredient).where(Ingredient.name.in_(ingredients))).all()
            for recipe in recipes:
                recipe.ingredients = session.scalars(select(Ingredient).join(RecipeIngredient).where(RecipeIngredient.recipe_id == recipe.id)).all()
            if not recipes:
                raise HTTPException(status_code=404, detail="No recipes found")
            return [RecipeResponse.model_validate(recipe) for recipe in recipes]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recipes by ingredients: {str(e)}")