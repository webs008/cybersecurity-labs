"""
recon.py
--------
CLI entry point for the passive recon pipeline.
Runs: crt.sh subdomain enumeration, Wayback Machine archived URLs,
SSL certificate check, then generates a consolidated markdown report.
"""

import argparse

from modules.crtsh import get_subdomains
from modules.wayback import get_archived_urls
from modules.ssl_check import check_ssl
from report import generate_report, save_report


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

    print()

    # --- Wayback Machine ---
    print(f"[*] Running Wayback Machine lookup for {args.domain}...")
    wayback_result = get_archived_urls(args.domain)

    if wayback_result["error"]:
        print(f"[!] Error: {wayback_result['error']}")
    else:
        print(f"[+] Found {wayback_result['count']} archived URLs:")
        for u in wayback_result["urls"][:20]:
            print(f"    {u}")
        if wayback_result["count"] > 20:
            print(f"    ... and {wayback_result['count'] - 20} more")

    print()

    # --- SSL/TLS Certificate ---
    print(f"[*] Checking SSL certificate for {args.domain}...")
    ssl_result = check_ssl(args.domain)

    if ssl_result["error"]:
        print(f"[!] Error: {ssl_result['error']}")
    else:
        print(f"[+] Issued to: {ssl_result['issued_to']}")
        print(f"    Issued by: {ssl_result['issued_by']}")
        print(f"    Expires: {ssl_result['expires']} ({ssl_result['days_remaining']} days remaining)")

    print()

    # --- Report Generation ---
    print("[*] Generating consolidated report...")
    report_text = generate_report(args.domain, crtsh_result, wayback_result, ssl_result)
    filepath = save_report(args.domain, report_text)
    print(f"[+] Report saved to: {filepath}")


if __name__ == "__main__":
    main()
