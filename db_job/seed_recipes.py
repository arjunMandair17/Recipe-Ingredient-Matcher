import requests
import string
from db.sql_init import get_session
from db.db_models import Recipe
from sqlalchemy import select

MEALDB_API = "https://www.themealdb.com/api/json/v1/1/"


def contains_n_ingredients(recipe: dict, n: int) -> bool:
    """Check if a recipe has at least n ingredients."""
    count = 0
    for key, value in recipe.items():
        if key.startswith("strIngredient"):
            count += 1
        if count >= n:
            return True
    return False

def is_valid_recipe(recipe: dict) -> bool:
    """Check if a recipe has valid metadata."""
    return contains_n_ingredients(recipe, 3) and recipe.get("strMeal") and recipe.get("strIngredient1") and recipe.get("strMeasure1") and recipe.get("strInstructions") and recipe.get("strMealThumb")

def fetch_recipes() -> dict[str, dict]:
    """Fetch every meal TheMealDB exposes via letter search. """
    recipes: dict[str, dict[str, str]] = {}
    for letter in string.ascii_lowercase:
        response: requests.Response = requests.get(f"{MEALDB_API}search.php?f={letter}")
        response.raise_for_status()

        meals = response.json().get("meals") or []

        for meal in meals:
            recipes[meal["idMeal"]] = meal ## stores the meal data with it's id as the key

    return recipes

def filter_recipes(recipes: dict[str, dict]) -> list[dict]:
    """Filter recipes to only include those with valid metadata."""
    valid_recipes: list[dict] = []

    for key, value in recipes.items():
        if is_valid_recipe(value):
        
            recipe = {
                "id": key,
                "name": value.get("strMeal") or "",
                "ingredients": [value.get(f"strIngredient{i}") for i in range(1, 21) if value.get(f"strIngredient{i}")],
                "instructions": value.get("strInstructions") or "",
                "image": value.get("strMealThumb") or "",
                "measures": [value.get(f"strMeasure{i}") for i in range(1, 21) if value.get(f"strMeasure{i}")]
            }
            valid_recipes.append(recipe)
    
    
    ## log the number of valid recipes
    print(f"Found {len(valid_recipes)} valid recipes")
    return valid_recipes

def seed_recipes() -> list[dict]:
    """Seed the database with recipes."""
    recipes = fetch_recipes()
    valid_recipes = filter_recipes(recipes)

    ## only insert recipes that are not already in the database
    valid_recipes = get_extra_recipes(valid_recipes)
    print(f"{len(valid_recipes)} recipes are not in the database yet")

    with get_session() as session:
        for recipe in valid_recipes:
            session.add(Recipe(
                api_id=recipe["id"],
                name=recipe["name"],
                image_url=recipe["image"],
                instructions=recipe["instructions"]
            ))
            
        session.commit()
    

    return (valid_recipes, len(valid_recipes))

def get_extra_recipes(recipes: list[dict]) -> list[dict]:
    """Check if the recipes are already seeded, returns recipes that are not in the database."""
    if not recipes:
        return []

    with get_session() as session:
        seeded = set(
            session.scalars(
                select(Recipe.api_id).where(
                    Recipe.api_id.in_([recipe["id"] for recipe in recipes])
                )
            ).all()
        )
        return [recipe for recipe in recipes if recipe["id"] not in seeded]


if __name__ == "__main__":
    (valid_recipes, num_recipes) = seed_recipes()
    print(f"Found {num_recipes} valid recipes")

    ingredients: set[str] = set()
    for recipe in valid_recipes:
        for ingredient in recipe["ingredients"]:
            ingredients.add(ingredient.lower().strip())
    
    print(f"Found {len(ingredients)} unique ingredients")