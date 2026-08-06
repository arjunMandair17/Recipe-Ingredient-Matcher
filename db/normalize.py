"""Shared ingredient name normalization for seeding and API search."""

ADJECTIVES = {
    "flat", "smoky", "fresh", "dry", "soft", "rough", "small", "large", "rare",
    "ready", "rolled", "clear", "unwaxed", "new", "dark", "chopped", "roasted",
    "of", "chilled", "smoked", "crusty", "ground", "hot", "cooking", "unsalted",
    "sprouting", "caramelized", "skirty", "dessicated", "light", "floury",
    "shelled", "freshly", "melted", "streaky", "boiling", "marinated",
    "strained", "flaked", "mixed", "fermented", "warm", "seasoned", "grated",
    "cold", "soured", "stale", "fine", "raw",
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
