import requests
from pluralizer import Pluralizer
API_URL = "http://localhost:8000"


def test_get_recipes():

    response = requests.post(f"{API_URL}/recipes/search", json={
        "ingredient_ids": [189, 340, 56]
    })

    print(response.json())







if __name__ == "__main__":
    
    test_get_recipes()