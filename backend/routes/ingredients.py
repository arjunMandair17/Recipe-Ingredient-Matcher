from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select

from backend.api_models import IngredientResponse
from db.sql_init import get_session
from db.db_models import Ingredient


ingredients_router = APIRouter(prefix="/ingredients", tags=["ingredients"])


@ingredients_router.get("/", response_model=list[IngredientResponse])
async def get_ingredients(
    name: str | None = Query(default=None, description="Optional case-insensitive name filter"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[IngredientResponse]:
    """Return ingredients with optional name filter and limit/offset pagination."""
    try:
        with get_session() as session:
            stmt = select(Ingredient).order_by(Ingredient.name)
            if name is not None:
                stmt = stmt.where(Ingredient.name.ilike(f"%{name.strip().lower()}%"))
            ingredients = session.scalars(stmt.limit(limit).offset(offset)).all()
            return [IngredientResponse.model_validate(row) for row in ingredients]
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
