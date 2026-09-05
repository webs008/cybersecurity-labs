"""
recon.py
--------
CLI entry point for the passive recon pipeline.
Runs: crt.sh + Subfinder subdomain enumeration (merged), httpx live-host
probing, Wayback Machine archived URLs, SSL certificate check, DNS
enumeration, WHOIS lookup, then generates a consolidated markdown report.
"""

import argparse

from modules.crtsh import get_subdomains
from modules.subfinder_lookup import find_subdomains
from modules.httpx_probe import probe_hosts
from modules.wayback import get_archived_urls
from modules.ssl_check import check_ssl
from modules.dns_enum import get_dns_records
from modules.whois_lookup import get_whois_info
from modules.virustotal_lookup import check_domain
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
        print(f"[+] Found {crtsh_result['count']} subdomains via crt.sh")

    print()

    # --- Subfinder ---
    print(f"[*] Running Subfinder for {args.domain}...")
    subfinder_result = find_subdomains(args.domain)

    if subfinder_result["error"]:
        print(f"[!] Error: {subfinder_result['error']}")
    else:
        print(f"[+] Found {subfinder_result['count']} subdomains via Subfinder")

    print()

    # --- Merge crt.sh and Subfinder results into one deduplicated list ---
    combined_subdomains = sorted(set(
        crtsh_result.get("subdomains", []) + subfinder_result.get("subdomains", [])
    ))
    print(f"[*] Combined unique subdomains: {len(combined_subdomains)}")
    for sub in combined_subdomains:
        print(f"    {sub}")

    print()

    # --- httpx (live host probing) ---
    print("[*] Probing combined subdomain list for live hosts...")
    if not combined_subdomains:
        httpx_result = {"probed": 0, "live": [], "error": "No subdomains available to probe."}
        print("[!] Skipped: no subdomains to probe.")
    else:
        httpx_result = probe_hosts(combined_subdomains)
        if httpx_result["error"]:
            print(f"[!] Error: {httpx_result['error']}")
        else:
            print(f"[+] {len(httpx_result['live'])} of {httpx_result['probed']} hosts are live:")
            for host in httpx_result["live"]:
                tech = ", ".join(host.get("tech", [])) or "none detected"
                print(f"    {host['url']} [{host['status_code']}] {host['title']} — Tech: {tech}")

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

    # --- DNS Records ---
    print(f"[*] Enumerating DNS records for {args.domain}...")
    dns_result = get_dns_records(args.domain)

    if dns_result["error"]:
        print(f"[!] Error: {dns_result['error']}")
    else:
        print(f"[+] MX records: {len(dns_result['mx'])}")
        for mx in dns_result["mx"]:
            print(f"    {mx}")
        print(f"[+] NS records: {len(dns_result['ns'])}")
        for ns in dns_result["ns"]:
            print(f"    {ns}")
        print(f"[+] SPF record found: {dns_result['spf_found']}")
        print(f"[+] DMARC record found: {dns_result['dmarc_found']}")

    print()

    # --- WHOIS ---
    print(f"[*] Running WHOIS lookup for {args.domain}...")
    whois_result = get_whois_info(args.domain)

    if whois_result["error"]:
        print(f"[!] Error: {whois_result['error']}")
    else:
        print(f"[+] Registrar: {whois_result['registrar']}")
        print(f"    Created: {whois_result['creation_date']}")
        print(f"    Expires: {whois_result['expiration_date']}")
        print(f"    Nameservers: {', '.join(whois_result['name_servers'])}")
    print()

    # --- VirusTotal ---
    print(f"[*] Checking VirusTotal reputation for {args.domain}...")
    vt_result = check_domain(args.domain)

    if vt_result["error"]:
        print(f"[!] Error: {vt_result['error']}")
    else:
        print(f"[+] Malicious: {vt_result['malicious']}, Suspicious: {vt_result['suspicious']}, "
              f"Harmless: {vt_result['harmless']}")


    print()

    # --- Report Generation ---
    print("[*] Generating consolidated report...")
    report_text = generate_report(
        args.domain, crtsh_result, subfinder_result, combined_subdomains,
        wayback_result, ssl_result, dns_result, whois_result, httpx_result, vt_result
    )
    filepath = save_report(args.domain, report_text)
    print(f"[+] Report saved to: {filepath}")


if __name__ == "__main__":
    main()
