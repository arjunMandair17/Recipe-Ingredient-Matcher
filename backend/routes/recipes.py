from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from backend.api_models import (
    IngredientResponse,
    RecipeResponse,
    RecipeSearchRequest,
)
from db.sql_init import get_session
from db.db_models import Recipe, Ingredient, RecipeIngredient
from db.normalize import search_query


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


def expand_ingredient_ids(session: Session, ingredient_ids: list[int]) -> list[int]:
    """Expand selected ids to include name variants (e.g. butter → unsalted butter)."""
    selected = session.scalars(
        select(Ingredient).where(Ingredient.id.in_(ingredient_ids))
    ).all()
    if not selected:
        return list(ingredient_ids)

    bases = {search_query(ing.name) for ing in selected}
    bases.discard("")
    # head noun only (last token): "king prawn" also matches via "prawn", not "king"
    for base in list(bases):
        parts = base.split()
        if len(parts) > 1 and len(parts[-1]) > 2:
            bases.add(parts[-1])
    if not bases:
        return list(ingredient_ids)

    matches = session.scalars(
        select(Ingredient.id).where(
            or_(*[Ingredient.name.ilike(f"%{base}%") for base in bases])
        )
    ).all()
    return list({*ingredient_ids, *matches})


def annotate_match_types(
    recipes: list[RecipeResponse],
    selected: list[Ingredient],
) -> list[RecipeResponse]:
    """Tag search hits as exact (same cleaned base) or partial (variant / head-noun)."""
    exact_bases = {search_query(ing.name) for ing in selected}
    exact_bases.discard("")
    annotated: list[RecipeResponse] = []
    for recipe in recipes:
        is_exact = any(
            search_query(ing.name) in exact_bases for ing in recipe.ingredients
        )
        annotated.append(
            recipe.model_copy(update={"match_type": "exact" if is_exact else "partial"})
        )
    return annotated


@recipes_router.get("/", response_model=list[RecipeResponse])
async def get_recipes(
    name: str | None = Query(default=None, description="Optional case-insensitive name filter"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[RecipeResponse]:
    """Return recipes ordered by name, with optional name filter and limit/offset pagination."""
    try:
        with get_session() as session:
            stmt = select(Recipe).order_by(Recipe.name)
            if name is not None:
                stmt = stmt.where(Recipe.name.ilike(f"%{name.strip()}%"))
            recipes = session.scalars(stmt.limit(limit).offset(offset)).all()
            return build_recipe_responses(session, list(recipes))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting recipes: {str(e)}")


@recipes_router.get("/{recipe_id}/ingredients", response_model=list[IngredientResponse])
async def get_recipe_ingredients(recipe_id: int) -> list[IngredientResponse]:
    """Return ingredients for a recipe. 404 only if the recipe itself is missing."""
    try:
        with get_session() as session:
            recipe = session.scalars(
                select(Recipe).where(Recipe.id == recipe_id)
            ).one_or_none()
            if not recipe:
                raise HTTPException(status_code=404, detail="Recipe not found")

            ingredients = session.scalars(
                select(Ingredient)
                .join(RecipeIngredient)
                .where(RecipeIngredient.recipe_id == recipe_id)
                .order_by(Ingredient.name)
            ).all()
            return [IngredientResponse.model_validate(row) for row in ingredients]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting recipe ingredients: {str(e)}",
        )


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


@recipes_router.post("/search", response_model=list[RecipeResponse])
async def fetch_recipes_by_ingredients(
    body: RecipeSearchRequest,
) -> list[RecipeResponse]:
    """Fetch recipes that use any of the given ingredient ids (including name variants)."""
    try:
        with get_session() as session:
            selected = session.scalars(
                select(Ingredient).where(Ingredient.id.in_(body.ingredient_ids))
            ).all()
            ingredient_ids = expand_ingredient_ids(session, body.ingredient_ids)
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
            return annotate_match_types(
                build_recipe_responses(session, list(recipes)),
                list(selected),
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching recipes by ingredients: {str(e)}",
        )
