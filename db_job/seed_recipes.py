import requests
import string

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

        meals = response.json()["meals"]

        for meal in meals:
            recipes[meal["idMeal"]] = meal ## stores the meal data with it's id as the key

    return recipes

def filter_recipes(recipes: dict[str, dict]) -> list[dict]:
    """Filter recipes to only include those with valid metadata."""
    valid_recipes: list[dict] = []

    for key, value in recipes.items():
        if is_valid_recipe(value):
            valid_recipes.append(value)
    

    ## check against StatCan
    
    ## log the number of valid recipes
    print(f"Found {len(valid_recipes)} valid recipes")
    return valid_recipes

def seed_recipes() -> list[dict]:
    """Seed the database with recipes."""
    recipes = fetch_recipes()
    valid_recipes = filter_recipes(recipes)

    ## add to database

    return valid_recipes

