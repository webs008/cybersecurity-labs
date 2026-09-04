"""
wayback.py
----------
Queries the Wayback Machine's CDX API for historical URLs archived
under a target domain. No auth required.
"""

import requests


def get_archived_urls(domain: str) -> dict:
    """
    Query the Wayback Machine for every URL ever archived under the
    given domain, and return the unique set.
    """
    # The CDX API is the Wayback Machine's URL index — built for exactly
    # this kind of bulk lookup, unlike scraping the calendar UI.
    url = "https://web.archive.org/cdx/search/cdx"
    params = {
        "url": f"{domain}/*",   # the /* means "everything under this domain"
        "output": "json",
        "collapse": "urlkey",   # dedupes near-identical URLs automatically
        "limit": 500,           # cap results so this stays fast for big domains
    }
    
    try:
        response = requests.get(url, params=params, timeout=45)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {
            "domain": domain,
            "urls": [],
            "count": 0,
            "error": f"Request to Wayback Machine failed: {e}",
        }

    try:
        data = response.json()
    except ValueError:
        return {
            "domain": domain,
            "urls": [],
            "count": 0,
            "error": "Wayback Machine returned no parseable data.",
        }

    # The CDX API returns a list of lists. The first row is a header
    # (e.g. ["urlkey", "timestamp", "original", ...]) — skip it.
    if len(data) <= 1:
        return {
            "domain": domain,
            "urls": [],
            "count": 0,
            "error": None,
        }

    header = data[0]
    original_index = header.index("original")

    urls = sorted(set(row[original_index] for row in data[1:]))

    return {
        "domain": domain,
        "urls": urls,
        "count": len(urls),
        "error": None,
    }


if __name__ == "__main__":
    import sys
    import json

    target = sys.argv[1] if len(sys.argv) > 1 else "example.com"
    result = get_archived_urls(target)
    print(json.dumps(result, indent=2))
