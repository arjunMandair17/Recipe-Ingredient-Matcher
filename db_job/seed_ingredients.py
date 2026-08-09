from .scrape_raw import average_price, scrape_many
from .scrape_api import scrape_with_api
from sqlalchemy import select
from datetime import datetime
from db.sql_init import get_session
from db.db_models import Ingredient, Recipe, RecipeIngredient
from db.normalize import canonicalize_ingredient, search_query


def get_ingredients(recipe: dict) -> list[str]:
    """Get recipe ingredients as canonical names (singularized, de-adjectived, aliased)."""
    ingredients = recipe.get("ingredients") or []
    return [canonicalize_ingredient(ingredient) for ingredient in ingredients]


def get_price(ingredient: str) -> float | None:
    """Try Algolia first, then Playwright average_price as fallback."""
    query = search_query(ingredient)
    try:
        price = scrape_with_api(query)
        if price is not None:
            return price
    except Exception as exc:
        print(f"API failed for {ingredient!r} (query={query!r}): {exc}")

    try:
        price = average_price(query)
        if price is not None:
            return price
    except Exception as exc:
        print(f"Playwright failed for {ingredient!r} (query={query!r}): {exc}")

    return None


def get_ingredient_prices(ingredients: list[str]) -> dict[str, float | None]:
    """Get prices for ingredients (API with Playwright fallback)."""
    return scrape_many(ingredients, function=get_price)


def seed_ingredients(recipes: list[dict]) -> tuple[dict[str, float | None], int, int]:
    """Seed unique canonical ingredients and link recipes to those shared rows."""
    ingredients: set[str] = set()
    for recipe in recipes:
        ingredients.update(get_ingredients(recipe))

    prices = get_ingredient_prices(list(ingredients))
    scrape_count = sum(1 for price in prices.values() if price is not None)

    if not ingredients:
        return (prices, 0, scrape_count)

    with get_session() as session:
        existing = {
            row.name: row
            for row in session.scalars(
                select(Ingredient).where(Ingredient.name.in_(ingredients))
            ).all()
        }

        now = datetime.now()
        for name in ingredients:
            if name in existing:
                existing[name].price = prices.get(name)
                existing[name].last_scraped = now
            else:
                row = Ingredient(
                    name=name,
                    price=prices.get(name),
                    last_scraped=now,
                )
                session.add(row)
                existing[name] = row

        session.flush()
        ingredient_ids = {name: row.id for name, row in existing.items()}
        session.commit()  ## keep the scraped prices even if linking fails

        ## only add links for recipes that do not already have connections
        recipe_ids = dict(session.execute(select(Recipe.api_id, Recipe.id)).all())
        linked = set(session.scalars(select(RecipeIngredient.recipe_id)).all())

        links = []
        for recipe in recipes:
            recipe_id = recipe_ids.get(recipe["id"])
            if recipe_id is None or recipe_id in linked:
                continue

            measures = recipe.get("measures") or []
            seen = set()  ## same canonical name can appear twice after normalization
            for i, name in enumerate(get_ingredients(recipe)):
                if name in seen:
                    continue
                seen.add(name)
                links.append(
                    RecipeIngredient(
                        recipe_id=recipe_id,
                        ingredient_id=ingredient_ids[name],
                        measure=measures[i] if i < len(measures) else None,
                    )
                )

        session.add_all(links)
        session.commit()

    return (prices, len(ingredients), scrape_count)
