from .seed_recipes import seed_recipes
from .seed_ingredients import seed_ingredients




def seed_job():
    try:
        (valid_recipes, num_recipes) = seed_recipes()
        (prices, num_ingredients, scrape_count) = seed_ingredients(valid_recipes)
        print(f"Seeded {num_recipes} recipes and {num_ingredients} ingredients.")
        print(f"{scrape_count} of the {num_ingredients} ingredients were scraped successfully.")
    except Exception as e:
        print(f"Error: {e}")
        raise e

if __name__ == "__main__":
    seed_job()