"""
crtsh.py
--------
Queries crt.sh (Certificate Transparency log search) for subdomains
tied to a target domain.
"""

import requests


def get_subdomains(domain: str) -> dict:
    """
    Query crt.sh for certificates issued for the given domain and
    extract the unique subdomains found.
    """
    url = f"https://crt.sh/?q=%25.{domain}&output=json"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # raises an error for 4xx/5xx responses
    except requests.exceptions.RequestException as e:
        # covers timeouts, connection errors, DNS failures, bad status codes
        return {
            "domain": domain,
            "subdomains": [],
            "count": 0,
            "error": f"Request to crt.sh failed: {e}",
        }

    try:
        data = response.json()
    except ValueError:
        # crt.sh sometimes returns an empty or malformed body
        return {
            "domain": domain,
            "subdomains": [],
            "count": 0,
            "error": "crt.sh returned no parseable data (domain may have no certs on record).",
        }

    subdomains = set()
    for entry in data:
        name_value = entry.get("name_value", "")
        for name in name_value.split("\n"):
            name = name.strip().lower()
            if name and "*" not in name:
                subdomains.add(name)

    return {
        "domain": domain,
        "subdomains": sorted(subdomains),
        "count": len(subdomains),
        "error": None,
    }


if __name__ == "__main__":
    import sys
    import json

    target = sys.argv[1] if len(sys.argv) > 1 else "example.com"
    result = get_subdomains(target)
    print(json.dumps(result, indent=2))
