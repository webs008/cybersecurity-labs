"""
report.py
---------
Takes results from the recon modules and writes a single,
consolidated markdown report to disk.
"""

from datetime import datetime


def generate_report(domain: str, crtsh_result: dict, subfinder_result: dict,
                     combined_subdomains: list, wayback_result: dict, ssl_result: dict,
                     dns_result: dict, whois_result: dict, httpx_result: dict) -> str:
    """
    Build a markdown-formatted report string from the results of
    each recon module.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = []
    lines.append(f"# Passive Recon Report: {domain}")
    lines.append(f"*Generated: {timestamp}*")
    lines.append("")

    # --- Executive Summary ---
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(f"- Subdomains (crt.sh): {crtsh_result.get('count', 0)}")
    lines.append(f"- Subdomains (Subfinder): {subfinder_result.get('count', 0)}")
    lines.append(f"- Combined unique subdomains: {len(combined_subdomains)}")

    if httpx_result.get("error"):
        lines.append("- Live host probing: skipped or failed")
    else:
        lines.append(f"- Live hosts confirmed: {len(httpx_result.get('live', []))} of {httpx_result.get('probed', 0)}")

    if wayback_result.get("error"):
        lines.append("- Archived URLs: lookup failed (see details below)")
    else:
        lines.append(f"- Archived URLs found: {wayback_result.get('count', 0)}")

    if ssl_result.get("error"):
        lines.append("- SSL certificate: could not be retrieved")
    else:
        lines.append(f"- SSL certificate expires: {ssl_result.get('expires')} "
                      f"({ssl_result.get('days_remaining')} days remaining)")

    if dns_result.get("error"):
        lines.append("- DNS records: lookup failed")
    else:
        lines.append(f"- SPF/DMARC configured: {dns_result['spf_found']} / {dns_result['dmarc_found']}")

    if whois_result.get("error"):
        lines.append("- WHOIS: lookup failed")
    else:
        lines.append(f"- Domain registered via: {whois_result['registrar']}")

    lines.append("")

    # --- Combined subdomains section ---
    lines.append("## Subdomains (Combined: crt.sh + Subfinder)")
    lines.append("")
    lines.append(f"**{len(combined_subdomains)}** unique subdomains found across both sources:")
    lines.append("")
    for sub in combined_subdomains:
        lines.append(f"- {sub}")
    lines.append("")

    # --- httpx section ---
    lines.append("## Live Host Probing (httpx)")
    lines.append("")
    if httpx_result.get("error"):
        lines.append(f"**Note:** {httpx_result['error']}")
    else:
        lines.append(f"Probed **{httpx_result['probed']}** combined subdomains — "
                      f"**{len(httpx_result['live'])}** responded as live:")
        lines.append("")
        lines.append("| URL | Status | Title | Server | Technologies |")
        lines.append("|---|---|---|---|---|")
        for host in httpx_result["live"]:
            title = (host.get("title") or "").replace("|", "-")
            tech = ", ".join(host.get("tech", [])) or "-"
            lines.append(f"| {host['url']} | {host['status_code']} | {title} | {host.get('webserver', '')} | {tech} |")
    lines.append("")

    # --- Wayback section ---
    lines.append("## Archived URLs (Wayback Machine)")
    lines.append("")
    if wayback_result.get("error"):
        lines.append(f"**Error:** {wayback_result['error']}")
    else:
        lines.append(f"Found **{wayback_result['count']}** archived URLs "
                      f"(showing first 20):")
        lines.append("")
        for u in wayback_result["urls"][:20]:
            lines.append(f"- {u}")
        if wayback_result["count"] > 20:
            lines.append(f"- ...and {wayback_result['count'] - 20} more")
    lines.append("")

    # --- SSL section ---
    lines.append("## SSL/TLS Certificate")
    lines.append("")
    if ssl_result.get("error"):
        lines.append(f"**Error:** {ssl_result['error']}")
    else:
        lines.append(f"- **Issued to:** {ssl_result['issued_to']}")
        lines.append(f"- **Issued by:** {ssl_result['issued_by']}")
        lines.append(f"- **Expires:** {ssl_result['expires']} "
                      f"({ssl_result['days_remaining']} days remaining)")
    lines.append("")

    # --- DNS section ---
    lines.append("## DNS Records")
    lines.append("")
    if dns_result.get("error"):
        lines.append(f"**Error:** {dns_result['error']}")
    else:
        lines.append(f"- **SPF record found:** {dns_result['spf_found']}")
        lines.append(f"- **DMARC record found:** {dns_result['dmarc_found']}")
        lines.append("")
        lines.append("**Mail servers (MX):**")
        for mx in dns_result["mx"]:
            lines.append(f"- {mx}")
        lines.append("")
        lines.append("**Nameservers (NS):**")
        for ns in dns_result["ns"]:
            lines.append(f"- {ns}")
        lines.append("")
        lines.append("**TXT records:**")
        for txt in dns_result["txt"]:
            lines.append(f"- `{txt}`")
    lines.append("")

    # --- WHOIS section ---
    lines.append("## WHOIS Registration")
    lines.append("")
    if whois_result.get("error"):
        lines.append(f"**Error:** {whois_result['error']}")
    else:
        lines.append(f"- **Registrar:** {whois_result['registrar']}")
        lines.append(f"- **Created:** {whois_result['creation_date']}")
        lines.append(f"- **Expires:** {whois_result['expiration_date']}")
        lines.append(f"- **Nameservers:** {', '.join(whois_result['name_servers'])}")
    lines.append("")

    return "\n".join(lines)


def save_report(domain: str, report_text: str) -> str:
    """
    Write the report to a file named after the domain and return the path.
    """
    filename = f"recon_report_{domain.replace('.', '_')}.md"
    with open(filename, "w") as f:
        f.write(report_text)
    return filename
