"""
shodan_lookup.py
----------------
Queries Shodan for exposed hosts/services tied to a search term or domain.
Requires a Shodan API key, loaded from a .env file (never hardcoded).
"""

import os

import shodan
from dotenv import load_dotenv

load_dotenv()  # reads .env in the current directory and loads it into os.environ


def search_shodan(query: str) -> dict:
    """
    Run a Shodan search for the given query string and return
    a summary of matching hosts.
    """
    api_key = os.getenv("SHODAN_API_KEY")

    if not api_key:
        return {
            "query": query,
            "results": [],
            "count": 0,
            "error": "SHODAN_API_KEY not found. Check your .env file.",
        }

    api = shodan.Shodan(api_key)

    try:
        results = api.search(query)
    except shodan.APIError as e:
        return {
            "query": query,
            "results": [],
            "count": 0,
            "error": f"Shodan API error: {e}",
        }

    hosts = []
    for match in results["matches"]:
        hosts.append({
            "ip": match.get("ip_str"),
            "port": match.get("port"),
            "org": match.get("org"),
            "product": match.get("product"),
        })

    return {
        "query": query,
        "results": hosts,
        "count": results.get("total", len(hosts)),
        "error": None,
    }


if __name__ == "__main__":
    import sys
    import json

    q = sys.argv[1] if len(sys.argv) > 1 else "apache"
    result = search_shodan(q)
    print(json.dumps(result, indent=2))
