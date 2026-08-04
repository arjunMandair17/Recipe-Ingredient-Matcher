from datetime import datetime

from pydantic import BaseModel, ConfigDict


class IngredientRequest(BaseModel):
    name: str


class IngredientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: float | None
    last_scraped: datetime | None = None


class RecipeRequest(BaseModel):
    api_id: str
    name: str
    image_url: str
    instructions: str


class RecipeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    image_url: str
    instructions: str
    ingredients: list[IngredientResponse] = []
