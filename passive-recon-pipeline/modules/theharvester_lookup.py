"""
theharvester_lookup.py
-----------------------
Wraps theHarvester CLI tool to gather emails, hosts, IPs, ASNs, and
interesting URLs from multiple OSINT sources in one pass.

Requires theHarvester to be installed and on PATH (ships with Kali by default).
"""

import json
import os
import subprocess
import tempfile


def gather_osint(domain: str, sources: str = "crtsh,otx,urlscan") -> dict:
    """
    Run theHarvester against the given domain and return discovered
    emails, hosts, IPs, ASNs, and interesting URLs.
    """
    # theHarvester writes to <name>.json rather than returning JSON on
    # stdout, so we use a temp file and read it back afterward.
    with tempfile.TemporaryDirectory() as tmpdir:
        output_base = os.path.join(tmpdir, "harvester_output")

        try:
            subprocess.run(
                ["theHarvester", "-d", domain, "-b", sources, "-f", output_base],
                capture_output=True,
                text=True,
                timeout=120,
            )
        except FileNotFoundError:
            return {
                "domain": domain,
                "emails": [], "hosts": [], "ips": [], "asns": [], "interesting_urls": [],
                "error": "theHarvester binary not found. Is it installed and on PATH?",
            }
        except subprocess.TimeoutExpired:
            return {
                "domain": domain,
                "emails": [], "hosts": [], "ips": [], "asns": [], "interesting_urls": [],
                "error": "theHarvester timed out for this domain.",
            }

        json_path = f"{output_base}.json"

        if not os.path.exists(json_path):
            return {
                "domain": domain,
                "emails": [], "hosts": [], "ips": [], "asns": [], "interesting_urls": [],
                "error": "theHarvester did not produce an output file.",
            }

        with open(json_path, "r") as f:
            data = json.load(f)

    return {
        "domain": domain,
        "emails": sorted(set(data.get("emails", []))),
        "hosts": sorted(set(data.get("hosts", []))),
        "ips": sorted(set(data.get("ips", []))),
        "asns": sorted(set(data.get("asns", []))),
        "interesting_urls": sorted(set(data.get("interesting_urls", []))),
        "error": None,
    }


if __name__ == "__main__":
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "example.com"
    result = gather_osint(target)
    print(json.dumps(result, indent=2))
