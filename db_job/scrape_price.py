"""Fetch visible Giant Tiger search prices for an ingredient and average them."""

import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from statistics import mean
from urllib.parse import quote_plus
from typing import Callable
from playwright.sync_api import sync_playwright
from scrape_test import scrape_with_api


PRICE_RE = re.compile(r"\$\s*(\d+(?:\.\d{1,2})?)")
DEFAULT_WORKERS = 5
DEFAULT_N = 10


def average_price(ingredient: str, n: int = DEFAULT_N) -> float | None:
    """Search Giant Tiger and average up to n matching product-tile prices."""
    url = f"https://www.gianttiger.com/search?q={quote_plus(ingredient)}&type=product"
    query = ingredient.casefold()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            extra_http_headers={"Referer": "https://www.google.com/"},
        )
        page.goto(url, wait_until="domcontentloaded", timeout=60_000)
        page.wait_for_timeout(5_000)

        if "Access Denied" in page.locator("body").inner_text():
            browser.close()
            raise RuntimeError("Giant Tiger blocked this request (bot protection). ")

        prices: list[float] = []
        for tile in page.locator("article.product-tile").all():
            if len(prices) >= n:
                break
            title = tile.locator(".product-tile__title").inner_text().casefold()
            if query not in title:
                continue
            text = tile.locator(".price__value").first.inner_text()
            match = PRICE_RE.search(text)
            if match:
                prices.append(float(match.group(1)))

        browser.close()

    return mean(prices) if prices else None


def scrape_many(
    ingredients: list[str], workers: int = DEFAULT_WORKERS, function: callable = scrape_with_api
) -> dict[str, float | None]:
    """Scrape average prices for many ingredients using a thread pool."""
    results: dict[str, float | None] = {}

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(function, item): item for item in ingredients}
        for future in as_completed(futures):
            item = futures[future]
            try:
                results[item] = future.result()
            except Exception as exc:  # noqa: BLE001 - surface per-item failures
                results[item] = None
                print(f"{item}: ERROR {exc}", flush=True)
            else:
                avg = results[item]
                if avg is None:
                    print(f"{item}: no prices", flush=True)
                else:
                    print(f"{item}: ${avg:.2f} avg", flush=True)

    return results


if __name__ == "__main__":
    # Comma-separated => threaded batch; otherwise a single query (may contain spaces).
    raw = " ".join(sys.argv[1:]) or "milk"
    queries = [q.strip() for q in raw.split(",") if q.strip()]

    if len(queries) == 1:
        try:
            avg = average_price(queries[0])
        except RuntimeError as exc:
            print(exc)
            sys.exit(2)
        if avg is None:
            print(f"No prices found for {queries[0]!r}")
            sys.exit(1)
        print(f"{queries[0]}: ${avg:.2f} avg")
    else:
        scrape_many(queries)
