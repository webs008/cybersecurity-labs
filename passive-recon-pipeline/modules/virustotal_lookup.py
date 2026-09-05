"""
virustotal_lookup.py
---------------------
Queries VirusTotal's domain report API for reputation data:
detection counts from security vendors, and categorization.
Requires a free VirusTotal API key, loaded from .env.
"""

import os

import requests
from dotenv import load_dotenv

load_dotenv()


def check_domain(domain: str) -> dict:
    """
    Query VirusTotal for reputation data on the given domain.
    """
    api_key = os.getenv("VIRUSTOTAL_API_KEY")

    if not api_key:
        return {
            "domain": domain,
            "malicious": None,
            "suspicious": None,
            "harmless": None,
            "reputation": None,
            "error": "VIRUSTOTAL_API_KEY not found. Check your .env file.",
        }

    url = f"https://www.virustotal.com/api/v3/domains/{domain}"
    headers = {"x-apikey": api_key}

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {
            "domain": domain,
            "malicious": None,
            "suspicious": None,
            "harmless": None,
            "reputation": None,
            "error": f"VirusTotal request failed: {e}",
        }

    data = response.json()
    attributes = data.get("data", {}).get("attributes", {})
    stats = attributes.get("last_analysis_stats", {})

    return {
        "domain": domain,
        "malicious": stats.get("malicious", 0),
        "suspicious": stats.get("suspicious", 0),
        "harmless": stats.get("harmless", 0),
        "reputation": attributes.get("reputation"),
        "error": None,
    }


if __name__ == "__main__":
    import sys
    import json

    target = sys.argv[1] if len(sys.argv) > 1 else "example.com"
    result = check_domain(target)
    print(json.dumps(result, indent=2))
