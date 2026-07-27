"""Fetch visible No Frills search prices for an ingredient and average them."""

import re
import sys
from statistics import mean
from urllib.parse import quote_plus

from playwright.sync_api import sync_playwright

PRICE_RE = re.compile(r"\$\s*(\d+(?:\.\d{1,2})?)")


def average_price(ingredient: str) -> float | None:
    """Search No Frills for an ingredient and return the average listed price."""
    url = f"https://www.nofrills.ca/search?search-bar={quote_plus(ingredient)}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            )
        )
        page.goto(url, wait_until="domcontentloaded", timeout=60_000)
        page.wait_for_timeout(5_000)

        body = page.locator("body").inner_text()
        browser.close()

    if "Access Denied" in body:
        raise RuntimeError(
            "No Frills blocked this request (bot protection). "
            "Automated scraping is unreliable for production."
        )

    prices = [float(m) for m in PRICE_RE.findall(body)]
    return mean(prices) if prices else None


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) or "milk"
    try:
        avg = average_price(query)
    except RuntimeError as exc:
        print(exc)
        sys.exit(2)

    if avg is None:
        print(f"No prices found for {query!r}")
        sys.exit(1)
    print(f"{query}: ${avg:.2f} avg")
