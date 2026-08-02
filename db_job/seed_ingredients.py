from scrape_raw import average_price, scrape_many
from scrape_api import scrape_with_api


def get_ingredients(recipe: dict) -> list[str]:
    """Get ingredients from a recipe."""
    ingredients = recipe.get("ingredients") or []
    return [ingredient.lower().strip() for ingredient in ingredients]


def get_price(ingredient: str) -> float | None:
    """Try Algolia first, then Playwright average_price as fallback."""
    try:
        price = scrape_with_api(ingredient)
        if price is not None:
            return price
    except Exception as exc:
        print(f"API failed for {ingredient!r}: {exc}")

    try:
        price = average_price(ingredient)
        if price is not None:
            return price
    except Exception as exc:
        print(f"Playwright failed for {ingredient!r}: {exc}")

    return None


def get_ingredient_prices(ingredients: list[str]) -> dict[str, float | None]:
    """Get prices for ingredients (API with Playwright fallback)."""
    return scrape_many(ingredients, function=get_price)


def seed_ingredients(recipes: list[dict]) -> tuple[dict[str, float | None], int]:
    """Seed the database with unique ingredients."""
    ingredients = set()  
    for recipe in recipes:
        ingredients.update(get_ingredients(recipe)) ## adds all ingredients from the current recipe
    prices = get_ingredient_prices(list(ingredients))

    ## add to database
    
    return (prices, len(ingredients))

