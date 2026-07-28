from pydantic import BaseModel

class IngredientRequest(BaseModel):
    name: str
    quantity: float
    unit: str


class IngredientResponse(BaseModel):
    name: str
    price: float
    price_url: str
    quantity: float
    unit: str


class RecipeRequest(BaseModel):
    api_id: str
    name: str
    image_url: str
    instructions: str

class RecipeResponse(BaseModel):
    id: int
    name: str
    image_url: str
    instructions: str
    ingredients: list[IngredientResponse]
