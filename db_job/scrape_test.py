"""Probe the Algolia product search API discovered in browser DevTools."""

import json
import sys

import requests

URL = "https://ngmhtyxt0t-3.algolianet.com/1/indexes/*/queries"
PARAMS = {
    "x-algolia-agent": "Algolia for JavaScript (5.49.1); Lite (5.49.1); Browser",
    "x-algolia-api-key": "1ec86e7ee6661988fb72e0c843badcd8",
    "x-algolia-application-id": "NGMHTYXT0T",
}

# Minimal clone of the main search request from DevTools (shopify_products / milk).
PAYLOAD = {
    "requests": [
        {
            "indexName": "shopify_products",
            "query": "milk",
            "facets": [
                "named_tags.badge_en",
                "price",
                "named_tags.L3_category_en",
                "named_tags.L4_category_en",
                "vendor",
                "product_type",
                "meta.english.grocery_product",
                "meta.info.store_inventory",
            ],
            "filters": "named_tags.shippable:true OR named_tags.mms_province_code:ON",
            "facetFilters": [],
            "numericFilters": [
                [
                    "meta.info.store_inventory.64619348029 >= 1",
                    "meta.info.store_inventory.online >= 1",
                ]
            ],
            "hitsPerPage": 30,
            "page": 0,
            "distinct": 1,
            "clickAnalytics": True,
            "getRankingInfo": True,
        }
    ]
}


def main() -> None:
    """POST the Algolia multi-query and print product name/price hits."""
    query = " ".join(sys.argv[1:]) or "milk"
    PAYLOAD["requests"][0]["query"] = query

    resp = requests.post(URL, params=PARAMS, json=PAYLOAD, timeout=30)
    print("status:", resp.status_code)
    resp.raise_for_status()

    data = resp.json()
    results = data.get("results") or []
    if not results:
        print("no results key:", json.dumps(data, indent=2)[:2000])
        return

    hits = results[0].get("hits") or []
    print(f"hits: {len(hits)} (nbHits={results[0].get('nbHits')})")

    def _safe(value: object) -> str:
        return str(value).encode("ascii", "replace").decode("ascii")

    for hit in hits[:10]:
        name = hit.get("title") or hit.get("name") or hit.get("product_type")
        price = hit.get("price")
        vendor = hit.get("vendor")
        handle = hit.get("handle")
        print(
            f"- {_safe(name)!r} | price={price} | "
            f"vendor={_safe(vendor)} | handle={_safe(handle)}"
        )

    if hits:
        print("\n--- sample hit keys ---")
        print(sorted(hits[0].keys()))
        print("\n--- sample hit (truncated) ---")
        sample = json.dumps(hits[0], indent=2, default=str)[:2500]
        print(sample.encode("ascii", "replace").decode("ascii"))


if __name__ == "__main__":
    main()
