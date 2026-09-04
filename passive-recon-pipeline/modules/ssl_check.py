"""
ssl_check.py
------------
Connects to a target domain on port 443 and pulls basic SSL/TLS
certificate details: issuer, subject, expiration date.
No API key needed — uses Python's built-in ssl and socket libraries.
"""

import socket
import ssl
from datetime import datetime, timezone


def check_ssl(domain: str, port: int = 443) -> dict:
    """
    Connect to the given domain over SSL/TLS and return certificate details.
    """
    context = ssl.create_default_context()

    try:
        with socket.create_connection((domain, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
    except (socket.timeout, socket.gaierror, ConnectionRefusedError, ssl.SSLError) as e:
        return {
            "domain": domain,
            "error": f"Connection failed: {e}",
        }

    # cert['issuer'] and cert['subject'] come back as nested tuples —
    # this flattens them into a simple dict for readability
    issuer = dict(x[0] for x in cert.get("issuer", []))
    subject = dict(x[0] for x in cert.get("subject", []))

    not_after = cert.get("notAfter")
    expires = None
    days_remaining = None
    if not_after:
        expires_dt = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
        expires = expires_dt.strftime("%Y-%m-%d")
        days_remaining = (expires_dt - datetime.now(timezone.utc).replace(tzinfo=None)).days

    return {
        "domain": domain,
        "issued_to": subject.get("commonName"),
        "issued_by": issuer.get("organizationName", issuer.get("commonName")),
        "expires": expires,
        "days_remaining": days_remaining,
        "error": None,
    }


if __name__ == "__main__":
    import sys
    import json

    target = sys.argv[1] if len(sys.argv) > 1 else "example.com"
    result = check_ssl(target)
    print(json.dumps(result, indent=2))
