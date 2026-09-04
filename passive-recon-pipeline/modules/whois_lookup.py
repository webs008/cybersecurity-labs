"""
whois_lookup.py
---------------
Queries WHOIS registration data for a target domain: registrar,
creation/expiration dates, and nameservers.
No API key needed — uses the python-whois library.
"""

import whois


def get_whois_info(domain: str) -> dict:
    """
    Query WHOIS data for the given domain and return key registration details.
    """
    try:
        data = whois.whois(domain)
    except Exception as e:
        # python-whois can raise several different exception types
        # depending on the registrar/TLD, so a broad catch is intentional here
        return {
            "domain": domain,
            "registrar": None,
            "creation_date": None,
            "expiration_date": None,
            "name_servers": [],
            "error": f"WHOIS lookup failed: {e}",
        }

    # WHOIS data is notoriously inconsistent — dates and nameservers can come
    # back as a single value OR a list, depending on the registrar. This
    # normalizes both cases.
    def first_or_none(value):
        if isinstance(value, list):
            return value[0] if value else None
        return value

    def as_list(value):
        if value is None:
            return []
        if isinstance(value, list):
            return sorted(set(v.lower() for v in value if v))
        return [value.lower()]

    creation = first_or_none(data.creation_date)
    expiration = first_or_none(data.expiration_date)

    return {
        "domain": domain,
        "registrar": data.registrar,
        "creation_date": str(creation) if creation else None,
        "expiration_date": str(expiration) if expiration else None,
        "name_servers": as_list(data.name_servers),
        "error": None,
    }


if __name__ == "__main__":
    import sys
    import json

    target = sys.argv[1] if len(sys.argv) > 1 else "example.com"
    result = get_whois_info(target)
    print(json.dumps(result, indent=2))
