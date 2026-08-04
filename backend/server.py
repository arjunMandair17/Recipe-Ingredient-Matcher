from fastapi import FastAPI, HTTPException
from sqlalchemy import select

from backend.routes.recipes import recipes_router
from backend.routes.ingredients import ingredients_router
from db.sql_init import get_session
from db.db_models import Recipe, Ingredient

app = FastAPI(title="Recipe API", description="API for recipes")


@app.get("/health")
async def health_check() -> dict:
    """Check if the server is running and the DB is reachable."""
    try:
        with get_session() as session:
            recipes = session.scalars(select(Recipe)).all()
            ingredients = session.scalars(select(Ingredient)).all()
        return {
            "status": "ok",
            "num_recipes": len(recipes),
            "num_ingredients": len(ingredients),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking health: {str(e)}")


app.include_router(recipes_router)
app.include_router(ingredients_router)
