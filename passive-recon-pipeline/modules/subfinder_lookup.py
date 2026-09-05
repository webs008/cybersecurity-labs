"""
subfinder_lookup.py
--------------------
Wraps ProjectDiscovery's subfinder CLI tool to enumerate subdomains
from multiple passive sources (crt.sh, DNS aggregators, and others
depending on configured API keys).

Requires subfinder to be installed and on PATH:
    go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
"""

import subprocess


def find_subdomains(domain: str) -> dict:
    """
    Run subfinder against the given domain and return the discovered
    subdomains as a sorted, deduplicated list.
    """
    try:
        result = subprocess.run(
            ["subfinder", "-d", domain, "-silent"],
            capture_output=True,
            text=True,
            timeout=90,
        )
    except FileNotFoundError:
        return {
            "domain": domain,
            "subdomains": [],
            "count": 0,
            "error": "subfinder binary not found. Is it installed and on PATH?",
        }
    except subprocess.TimeoutExpired:
        return {
            "domain": domain,
            "subdomains": [],
            "count": 0,
            "error": "subfinder timed out for this domain.",
        }

    subdomains = sorted(set(
        line.strip().lower()
        for line in result.stdout.strip().split("\n")
        if line.strip()
    ))

    return {
        "domain": domain,
        "subdomains": subdomains,
        "count": len(subdomains),
        "error": None,
    }


if __name__ == "__main__":
    import sys
    import json

    target = sys.argv[1] if len(sys.argv) > 1 else "example.com"
    result = find_subdomains(target)
    print(json.dumps(result, indent=2))
