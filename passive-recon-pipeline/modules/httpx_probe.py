"""
httpx_probe.py
--------------
Wraps ProjectDiscovery's httpx CLI tool to probe a list of hosts
and determine which are actually live, along with basic HTTP info
(status code, title, technologies where detected).

Requires httpx to be installed and on PATH:
    go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
"""

import json
import subprocess


def probe_hosts(hosts: list) -> dict:
    """
    Run httpx against a list of hostnames/subdomains and return
    which ones are live, with basic metadata for each.
    """
    if not hosts:
        return {
            "probed": 0,
            "live": [],
            "error": "No hosts provided to probe.",
        }

    # httpx reads hosts from stdin, one per line, and can output
    # structured JSON with -json for easy parsing.
    input_data = "\n".join(hosts)

    try:
        result = subprocess.run(
            ["httpx", "-silent", "-json", "-timeout", "10"],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=120,  # overall safety net for the whole batch
        )
    except FileNotFoundError:
        return {
            "probed": len(hosts),
            "live": [],
            "error": "httpx binary not found. Is it installed and on PATH?",
        }
    except subprocess.TimeoutExpired:
        return {
            "probed": len(hosts),
            "live": [],
            "error": "httpx probe timed out for this batch of hosts.",
        }

    live_hosts = []
    # httpx -json outputs one JSON object per line, one per live host
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        try:
            entry = json.loads(line)
            live_hosts.append({
                "url": entry.get("url"),
                "status_code": entry.get("status_code"),
                "title": entry.get("title"),
                "webserver": entry.get("webserver"),
            })
        except json.JSONDecodeError:
            continue  # skip any malformed line rather than crashing the batch

    return {
        "probed": len(hosts),
        "live": live_hosts,
        "error": None,
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        targets = sys.argv[1:]
    else:
        targets = ["hackthebox.com", "example.com"]

    result = probe_hosts(targets)
    print(json.dumps(result, indent=2))
