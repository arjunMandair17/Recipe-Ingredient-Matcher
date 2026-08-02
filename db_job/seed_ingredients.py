from scrape_raw import average_price, scrape_many
from scrape_api import scrape_with_api
from sqlalchemy import select

from db.sql_init import get_session
from db.db_models import Ingredient, Recipe, RecipeIngredient


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
    """Seed the database with unique ingredients and recipe links."""
    ingredients = set()
    for recipe in recipes:
        ingredients.update(get_ingredients(recipe))  ## adds all ingredients from the current recipe
    prices = get_ingredient_prices(list(ingredients))

    ## add ingredients to database (one flush for all IDs)
    with get_session() as session:
        rows = [
            Ingredient(name=name, price=prices[name])
            for name in ingredients
        ]
        session.add_all(rows)
        session.flush()
        ingredient_ids = {row.name: row.id for row in rows}
        session.commit()

    ## add ingredient connections to database
    with get_session() as session:
        # one query: MealDB api_id -> postgres recipe.id
        recipe_ids = dict(session.execute(select(Recipe.api_id, Recipe.id)).all())

        links = []
        for recipe in recipes:
            recipe_id = recipe_ids.get(recipe["id"])
            if recipe_id is None:
                continue

            measures = recipe.get("measures") or []
            for i, name in enumerate(get_ingredients(recipe)):
                links.append(
                    RecipeIngredient(
                        recipe_id=recipe_id,
                        ingredient_id=ingredient_ids[name],
                        measure=measures[i] if i < len(measures) else None,
                    )
                )

        session.add_all(links)
        session.commit()

    return (prices, len(ingredients))
