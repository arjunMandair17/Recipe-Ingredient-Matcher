import requests
import string

MEALDB_API = "https://www.themealdb.com/api/json/v1/1/"

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
        if value.get("strMeal") and value.get("strIngredient1") and value.get("strMeasure1") and value.get("strInstructions") and value.get("strMealThumb"):
            valid_recipes.append(value)
    return valid_recipes

def seed_recipes() -> list[dict]:
    """Seed the database with recipes."""
    recipes = fetch_recipes()
    valid_recipes = filter_recipes(recipes)
    return valid_recipes

