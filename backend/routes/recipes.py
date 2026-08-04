from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.api_models import IngredientResponse, RecipeResponse
from db.sql_init import get_session
from db.db_models import Recipe, Ingredient, RecipeIngredient


recipes_router = APIRouter(prefix="/recipes", tags=["recipes"])


def build_recipe_responses(session: Session, recipes: list[Recipe]) -> list[RecipeResponse]:
    """Build RecipeResponse list with ingredients loaded in one query."""
    if not recipes:
        return []

    recipe_ids = [recipe.id for recipe in recipes]

    # One query: all (recipe_id, Ingredient) pairs for the given recipes,
    # joined through recipe_ingredients on ingredient_id.
    rows = session.execute(
        select(RecipeIngredient.recipe_id, Ingredient)
        .join(Ingredient, Ingredient.id == RecipeIngredient.ingredient_id)
        .where(RecipeIngredient.recipe_id.in_(recipe_ids))
        .order_by(Ingredient.name)
    ).all()

    # Group those ingredients under each recipe_id for O(1) lookup below.
    ingredients_by_recipe: dict[int, list[Ingredient]] = {
        recipe_id: [] for recipe_id in recipe_ids
    }
    for recipe_id, ingredient in rows:
        ingredients_by_recipe[recipe_id].append(ingredient)

    # Build one RecipeResponse per recipe, nesting its IngredientResponses.
    return [
        RecipeResponse(
            id=recipe.id,
            name=recipe.name,
            image_url=recipe.image_url,
            instructions=recipe.instructions,
            ingredients=[
                IngredientResponse.model_validate(ingredient)
                for ingredient in ingredients_by_recipe[recipe.id]
            ],
        )
        for recipe in recipes
    ]


@recipes_router.get("/", response_model=list[RecipeResponse])
async def get_recipes() -> list[RecipeResponse]:
    """Return all recipes ordered by name."""
    try:
        with get_session() as session:
            recipes = session.scalars(select(Recipe).order_by(Recipe.name)).all()
            if not recipes:
                raise HTTPException(status_code=404, detail="No recipes found")
            return build_recipe_responses(session, list(recipes))
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
            if not recipe:
                raise HTTPException(status_code=404, detail="Recipe not found")
            return build_recipe_responses(session, [recipe])[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting recipe: {str(e)}")


@recipes_router.post("/", response_model=list[RecipeResponse])
async def fetch_recipes_by_ingredients(
    ingredient_ids: list[int],
) -> list[RecipeResponse]:
    """Fetch recipes that use any of the given ingredient ids."""
    try:
        if not ingredient_ids:
            raise HTTPException(status_code=400, detail="No ingredient ids provided")

        with get_session() as session:
            recipes = session.scalars(
                select(Recipe)
                .where(
                    Recipe.id.in_(
                        select(RecipeIngredient.recipe_id).where(
                            RecipeIngredient.ingredient_id.in_(ingredient_ids)
                        )
                    )
                )
                .order_by(Recipe.name)
            ).all()
            if not recipes:
                raise HTTPException(status_code=404, detail="No recipes found")
            return build_recipe_responses(session, list(recipes))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching recipes by ingredients: {str(e)}",
        )
