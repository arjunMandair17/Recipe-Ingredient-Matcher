from fastapi import APIRouter, HTTPException
from backend.api_models import IngredientResponse, IngredientRequest
from db.sql_init import get_session
from pydantic import BaseModel
from sqlalchemy import select
from db.db_models import Ingredient, RecipeIngredient


ingredients_router = APIRouter(prefix="/ingredients", tags=["ingredients"])

@ingredients_router.get("/")
async def get_ingredients(response_model=list[IngredientResponse]) -> list[IngredientResponse]:
    # return all ingredients from the database
    try:
        with get_session() as session:
            result = session.execute(select(Ingredient).order_by(Ingredient.name)).all()
            if not result:
                raise HTTPException(status_code=404, detail="No ingredients found")
            session.commit()
            return [response_model.model_validate(row._asdict()) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
  


@ingredients_router.get("/")
async def get_ingredient(ingredient_id: int, recipe_id: int, response_model=IngredientResponse) -> IngredientResponse:
    try:
        with get_session() as session:

            if ingredient_id and recipe_id:
                raise HTTPException(status_code=400, detail="Both ingredient and recipe IDs cannot be provided")

            if ingredient_id:   # if the user provides an ingredient ID, return it
                result = session.scalars(select(Ingredient).where(Ingredient.id == ingredient_id)).one_or_none()
                if not result:  
                    raise HTTPException(status_code=404, detail="Ingredient not found")
                session.commit()
                return response_model.model_validate(result._asdict())


            elif recipe_id:   # if the user provides a recipe ID, return all ingredients for that recipe
                result = session.execute(select(Ingredient).join(RecipeIngredient).where(RecipeIngredient.recipe_id == recipe_id)).all()
                if not result:
                    raise HTTPException(status_code=404, detail="No ingredients found for recipe ID: " + str(recipe_id))
                session.commit()
                return [response_model.model_validate(row._asdict()) for row in result]

            else:
                raise HTTPException(status_code=400, detail="No ingredient or recipe ID provided")
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))