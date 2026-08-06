from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


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
    # set by /recipes/search: exact = cleaned name match, partial = variant/head-noun match
    match_type: Literal["exact", "partial"] | None = None


class RecipeSearchRequest(BaseModel):
    ingredient_ids: list[int] = Field(min_length=1)
