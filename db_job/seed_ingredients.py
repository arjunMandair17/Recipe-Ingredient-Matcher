import requests
import string
from scrape_price import scrape_many, average_price
from scrape_test import scrape_with_api
from seed_recipes import seed_recipes


def get_ingredients(recipe: dict) -> list[str]:
    """Get ingredients from recipes."""

    ingredients = recipe.get("ingredients")
    
    filtered_ingredients = [ingredient.lower().strip() for ingredient in ingredients]

    return filtered_ingredients


def get_ingredient_prices(ingredients: list[str]) -> list[dict]:
    """Get prices for ingredients."""

    prices = scrape_many(ingredients, function=scrape_with_api)

    return prices