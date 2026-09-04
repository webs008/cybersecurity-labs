"""
dns_enum.py
-----------
Queries common DNS record types for a target domain: MX, TXT, NS,
and SPF/DMARC (which live inside TXT records).
No API key needed — uses direct DNS queries via dnspython.
"""

import dns.resolver


def get_dns_records(domain: str) -> dict:
    """
    Query MX, TXT, and NS records for the given domain, and flag
    whether SPF and DMARC records are present within the TXT records.
    """
    result = {
        "domain": domain,
        "mx": [],
        "ns": [],
        "txt": [],
        "spf_found": False,
        "dmarc_found": False,
        "error": None,
    }

    # --- MX records (mail servers) ---
    try:
        answers = dns.resolver.resolve(domain, "MX")
        result["mx"] = sorted(str(r.exchange).rstrip(".") for r in answers)
    except dns.resolver.NoAnswer:
        pass  # domain has no MX records — not an error, just no mail server
    except dns.resolver.NXDOMAIN:
        result["error"] = f"Domain {domain} does not exist."
        return result
    except dns.exception.DNSException as e:
        result["error"] = f"MX lookup failed: {e}"

    # --- NS records (nameservers) ---
    try:
        answers = dns.resolver.resolve(domain, "NS")
        result["ns"] = sorted(str(r.target).rstrip(".") for r in answers)
    except dns.resolver.NoAnswer:
        pass
    except dns.exception.DNSException as e:
        if not result["error"]:
            result["error"] = f"NS lookup failed: {e}"

    # --- TXT records (includes SPF, and hints at DMARC's separate record) ---
    try:
        answers = dns.resolver.resolve(domain, "TXT")
        txt_records = [b"".join(r.strings).decode("utf-8", errors="ignore") for r in answers]
        result["txt"] = txt_records
        result["spf_found"] = any(txt.startswith("v=spf1") for txt in txt_records)
    except dns.resolver.NoAnswer:
        pass
    except dns.exception.DNSException as e:
        if not result["error"]:
            result["error"] = f"TXT lookup failed: {e}"

    # --- DMARC record (lives at _dmarc.<domain>, not the root domain) ---
    try:
        dmarc_domain = f"_dmarc.{domain}"
        answers = dns.resolver.resolve(dmarc_domain, "TXT")
        dmarc_records = [b"".join(r.strings).decode("utf-8", errors="ignore") for r in answers]
        result["dmarc_found"] = any(txt.startswith("v=DMARC1") for txt in dmarc_records)
    except dns.exception.DNSException:
        pass  # no DMARC record found — common, not necessarily an error

    return result


if __name__ == "__main__":
    import sys
    import json

    target = sys.argv[1] if len(sys.argv) > 1 else "example.com"
    result = get_dns_records(target)
    print(json.dumps(result, indent=2))
