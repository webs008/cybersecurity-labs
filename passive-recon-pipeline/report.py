"""
report.py
---------
Takes results from the recon modules and writes a single,
consolidated markdown report to disk.
"""

from datetime import datetime


def generate_report(domain: str, crtsh_result: dict, wayback_result: dict, ssl_result: dict) -> str:
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
    lines.append(f"- Subdomains discovered: {crtsh_result.get('count', 0)}")

    if wayback_result.get("error"):
        lines.append("- Archived URLs: lookup failed (see details below)")
    else:
        lines.append(f"- Archived URLs found: {wayback_result.get('count', 0)}")

    if ssl_result.get("error"):
        lines.append("- SSL certificate: could not be retrieved")
    else:
        lines.append(f"- SSL certificate expires: {ssl_result.get('expires')} "
                      f"({ssl_result.get('days_remaining')} days remaining)")
    lines.append("")

    # --- crt.sh section ---
    lines.append("## Subdomains (Certificate Transparency — crt.sh)")
    lines.append("")
    if crtsh_result.get("error"):
        lines.append(f"**Error:** {crtsh_result['error']}")
    else:
        lines.append(f"Found **{crtsh_result['count']}** subdomains:")
        lines.append("")
        for sub in crtsh_result["subdomains"]:
            lines.append(f"- {sub}")
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

    return "\n".join(lines)


def save_report(domain: str, report_text: str) -> str:
    """
    Write the report to a file named after the domain and return the path.
    """
    filename = f"recon_report_{domain.replace('.', '_')}.md"
    with open(filename, "w") as f:
        f.write(report_text)
    return filename
