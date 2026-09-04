"""
recon.py
--------
CLI entry point for the passive recon pipeline.
Currently wired to: crt.sh subdomain enumeration.
"""

import argparse

from modules.crtsh import get_subdomains


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

    print(f"[*] Running crt.sh subdomain lookup for {args.domain}...")
    result = get_subdomains(args.domain)

    if result["error"]:
        print(f"[!] Error: {result['error']}")
    else:
        print(f"[+] Found {result['count']} subdomains:")
        for sub in result["subdomains"]:
            print(f"    {sub}")


if __name__ == "__main__":
    main()
