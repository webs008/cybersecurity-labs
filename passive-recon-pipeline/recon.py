"""
recon.py
--------
CLI entry point for the passive recon pipeline.
Currently wired to: crt.sh subdomain enumeration, Wayback Machine archived URLs.
"""

import argparse

from modules.crtsh import get_subdomains
from modules.wayback import get_archived_urls


def main():
    parser = argparse.ArgumentParser(
        description="Run passive reconnaissance checks against a target domain."
    )
    parser.add_argument(
        "--domain",
        required=True,
        help="Target domain to run recon against (e.g. example.com)",
    )
    args = parser.parse_args()

    # --- crt.sh ---
    print(f"[*] Running crt.sh subdomain lookup for {args.domain}...")
    crtsh_result = get_subdomains(args.domain)

    if crtsh_result["error"]:
        print(f"[!] Error: {crtsh_result['error']}")
    else:
        print(f"[+] Found {crtsh_result['count']} subdomains:")
        for sub in crtsh_result["subdomains"]:
            print(f"    {sub}")

    print()  # blank line between sections for readability

    # --- Wayback Machine ---
    print(f"[*] Running Wayback Machine lookup for {args.domain}...")
    wayback_result = get_archived_urls(args.domain)

    if wayback_result["error"]:
        print(f"[!] Error: {wayback_result['error']}")
    else:
        print(f"[+] Found {wayback_result['count']} archived URLs:")
        for u in wayback_result["urls"][:20]:  # show first 20 only, can be huge
            print(f"    {u}")
        if wayback_result["count"] > 20:
            print(f"    ... and {wayback_result['count'] - 20} more")


if __name__ == "__main__":
    main()
