"""Shared ingredient name normalization for seeding and API search."""

## adjectives to drop for consistency during scraping/seeding
ADJECTIVES = {
    "flat", "smoky", "fresh", "dry", "soft", "rough", "small", "large", "rare",
    "ready", "rolled", "clear", "unwaxed", "new", "dark", "chopped", "roasted",
    "of", "chilled", "smoked", "crusty", "ground", "hot", "cooking", "unsalted",
    "sprouting", "caramelized", "skirty", "dessicated", "light", "floury",
    "shelled", "freshly", "melted", "streaky", "boiling", "marinated",
    "strained", "flaked", "mixed", "fermented", "warm", "seasoned", "grated",
    "cold", "soured", "stale", "fine", "raw", "salted", "beaten"
}

## words that will slip through adjective filtering due to specificity, and must be mapped correctly
ALIASES = { 
    "frozen prawn": "prawn", "banana": "banana fruit", "hummu": "hummus", "coriander": "cilantro", 
    "green olive": "green olive slice", "coriander leave": "cilantro leave", "yoghurt": "yogurt",
    "natural yoghurt": "yogurt"
    }

## words to never expand on during matching
DENYLIST = {
    "sauce", "oil", "mix", "paste", "powder", "juice", "concentrate", "liquid",
    "spice", "herb", "flavor", "seasoning","seed", "rub", "all-purpose", 
    "all purpose", "essence", "extract", "flour", "baked", "baby", "new", "fillet",
    "bean", "cutlet", "sprout", "gravy", "tenderloin", "jam", "roll", "sugar", "wheat",
    "leave", "nut", "leg", "flake", "roast", "stick", "cream", "red", "king", "green",
    "yellow", "white", "black", "purple", "orange", "brown", "blue", "gold", 
}


def singularize(word: str) -> str:
    """Best-effort singular form for one ingredient token."""
    if word.endswith("ies") and len(word) > 4:
        return word[:-3] + "y"
    if word.endswith(("ches", "shes", "sses", "xes", "zes")):
        return word[:-2]
    if word.endswith("s") and not word.endswith("ss") and len(word) > 3:
        return word[:-1]
    return word


def search_query(ingredient: str) -> str:
    """Drop adjective tokens for matching/scraping."""
    cleaned = " ".join(
        word for word in ingredient.lower().split() if word not in ADJECTIVES
    )
    return cleaned or ingredient.lower()


def canonicalize_ingredient(ingredient: str) -> str:
    """Singularize, drop adjectives, then apply aliases to a canonical DB name."""
    singular = " ".join(
        singularize(word) for word in ingredient.lower().strip().split() if word
    )
    cleaned = search_query(singular)
    return ALIASES.get(cleaned, cleaned)
