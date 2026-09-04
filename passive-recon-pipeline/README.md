# Passive Recon Pipeline

A command-line tool that runs multiple passive reconnaissance checks against a domain and outputs one consolidated markdown report — instead of manually running several separate tools and copy-pasting results together.

## What it does

Given a single domain, the pipeline runs:

1. **Subdomain enumeration** via [crt.sh](https://crt.sh) (Certificate Transparency log search)
2. **Historical URL discovery** via the [Wayback Machine](https://web.archive.org) CDX API
3. **SSL/TLS certificate inspection** — issuer, subject, and expiration, pulled via a direct TLS handshake (no API key required)

All three run in a single command, print live progress to the terminal, and generate one consolidated markdown report saved to disk.

## Why passive recon

Every check in this pipeline is passive — nothing is sent to the target beyond what a normal browser or search engine already would. No port scanning, no active probing. This mirrors the first phase of a real penetration test methodology: understanding what's publicly discoverable about a target before ever touching its infrastructure directly.

## Usage

```bash
python3 recon.py --domain example.com
```

This prints results for each module as it runs, then writes a report to:

```
recon_report_example_com.md
```

## Project structure

```
passive-recon-pipeline/
├── recon.py              # CLI entry point (argparse-based)
├── report.py             # Builds and saves the consolidated markdown report
├── modules/
│   ├── crtsh.py           # Certificate Transparency subdomain enumeration
│   ├── wayback.py         # Wayback Machine archived URL lookup
│   ├── ssl_check.py       # SSL/TLS certificate inspection
│   └── shodan_lookup.py   # Shodan search integration (requires a paid Shodan API tier)
├── requirements.txt
└── README.md
```

## Setup

```bash
git clone <this-repo-url>
cd passive-recon-pipeline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Design notes

- Every module returns a consistent dictionary shape (`{"error": None, ...}` or a populated `"error"` message), so failures are handled gracefully and reported clearly rather than crashing the whole pipeline mid-run.
- Modules are independent and can be imported and used on their own — each has a `if __name__ == "__main__":` block for standalone testing.
- API keys (used by the Shodan module) are loaded from a local `.env` file via `python-dotenv` and are never hardcoded or committed to version control.

## Known limitations

- The **Shodan module** is fully written but requires a paid Shodan API tier — free/OSS-tier accounts have zero query credits and will return a 403 error on search.
- The **Wayback Machine module** occasionally hits rate limiting or temporary 503 errors from the Internet Archive's public API during high-traffic periods; the pipeline handles this gracefully and reports the error in the final output rather than failing the whole run.
- Currently scoped to single-domain lookups; no bulk/batch mode yet.

## Roadmap

- [ ] Wire in the Shodan module once API access is available
- [ ] Add an Nmap module for the active-recon phase (separate from this passive-only tool, but designed to feed the same report format)
- [ ] HTML report export in addition to markdown
- [ ] Optional PDF export for client-ready deliverables

## Disclaimer

This tool is intended for authorized security research and reconnaissance on domains you own or have explicit permission to test. All checks are passive, but always confirm scope and authorization before running any reconnaissance activity against a third party.

---

*Built as part of an ongoing cybersecurity learning journey — see the [Cisco Ethical Hacker lab writeups](../penetration-testing/) in this repo for the manual, tool-by-tool version of these same techniques.*
