# Passive Recon Pipeline

A command-line tool that runs eight passive reconnaissance checks against a domain and outputs one consolidated markdown report — instead of manually running several separate tools and copy-pasting results together.

## What it does

Given a single domain, the pipeline runs:

1. **Subdomain enumeration** via [crt.sh](https://crt.sh) (Certificate Transparency logs) **and** [Subfinder](https://github.com/projectdiscovery/subfinder) (aggregates multiple passive sources) — results are merged and deduplicated into one combined list
2. **Live host probing** via [httpx](https://github.com/projectdiscovery/httpx) — filters the combined subdomain list down to confirmed live hosts, with status codes, page titles, server fingerprinting, and detected technologies (frameworks, CMS platforms, JS libraries) per host
3. **Historical URL discovery** via the [Wayback Machine](https://web.archive.org) CDX API
4. **SSL/TLS certificate inspection** — issuer, subject, and expiration, pulled via a direct TLS handshake (no API key required)
5. **DNS enumeration** — MX, NS, and TXT records, with automatic SPF and DMARC detection
6. **WHOIS lookup** — registrar, creation/expiration dates, and nameservers
7. **VirusTotal reputation check** — malicious/suspicious/harmless verdict counts aggregated across dozens of security vendors

All checks run in a single command, print live progress to the terminal, and generate one consolidated markdown report saved to disk.

## Why passive recon

Every check in this pipeline is passive — nothing beyond a single live-host probe (httpx) touches the target more than a normal browser or search engine already would. No port scanning, no active exploitation attempts. This mirrors the first phase of a real penetration test methodology: understanding what's publicly discoverable about a target before ever touching its infrastructure directly.

## Usage

```bash
python3 recon.py --domain example.com
```

This prints progress for each module as it runs, then writes a report to:

```
recon_report_example_com.md
```

## Project structure

```
passive-recon-pipeline/
├── recon.py                  # CLI entry point (argparse-based)
├── report.py                 # Builds and saves the consolidated markdown report
├── modules/
│   ├── crtsh.py                # Certificate Transparency subdomain enumeration
│   ├── subfinder_lookup.py     # Subfinder CLI wrapper (subprocess) — multi-source subdomain enum
│   ├── httpx_probe.py          # httpx CLI wrapper (subprocess) — live host probing + tech detection
│   ├── wayback.py               # Wayback Machine archived URL lookup
│   ├── ssl_check.py             # SSL/TLS certificate inspection
│   ├── dns_enum.py              # DNS record enumeration (MX/NS/TXT/SPF/DMARC)
│   ├── whois_lookup.py          # WHOIS registration data
│   ├── virustotal_lookup.py     # VirusTotal domain reputation check
│   └── shodan_lookup.py         # Shodan search integration (requires a paid Shodan API tier)
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

### External CLI tools (required, installed via Go)

Two modules wrap external Go-based CLI tools rather than calling an HTTP API directly:

```bash
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

Make sure Go's bin directory is on your PATH **before** any other directory that might contain a conflicting binary of the same name (Kali ships its own unrelated `httpx` package by default):

```bash
export PATH=$(go env GOPATH)/bin:$PATH
```

### API keys

Create a `.env` file in the project root (never committed — see `.gitignore`):

```
VIRUSTOTAL_API_KEY=your_key_here
SHODAN_API_KEY=your_key_here
```

VirusTotal's free tier is sufficient for this tool. Shodan's free/OSS tier has zero query credits and will not work with the search-based module included here — a paid tier is required for that specific module.

## Design notes

- Every module returns a consistent dictionary shape (`{"error": None, ...}` or a populated `"error"` message), so failures are handled gracefully and reported clearly rather than crashing the whole pipeline mid-run.
- Modules are independent and can be imported and used on their own — each has an `if __name__ == "__main__":` block for standalone testing.
- Two modules (`httpx_probe.py`, `subfinder_lookup.py`) wrap external Go-based CLI tools via `subprocess` rather than calling an HTTP API directly — demonstrating integration beyond simple REST calls.
- API keys are loaded from a local `.env` file via `python-dotenv` and are never hardcoded or committed to version control.
- Subdomain sources are deliberately combined (crt.sh + Subfinder) rather than run independently, since different passive sources consistently surface different subdomains — testing against a real target showed Subfinder alone finding roughly double what crt.sh found on its own, with several unique results from each.

## Known limitations

- The **Shodan module** is fully written but requires a paid Shodan API tier — free/OSS-tier accounts have zero query credits and return a 403 error on search.
- The **Wayback Machine module** occasionally hits rate limiting or temporary 503 errors from the Internet Archive's public API during high-traffic periods; the pipeline handles this gracefully and reports the error in the final output rather than failing the whole run.
- Currently scoped to single-domain lookups; no bulk/batch mode yet.
- VirusTotal's free tier has a rate limit (4 requests/minute) — fine for single-domain runs, but would need throttling for batch use.

## Roadmap

- [ ] Wire in the Shodan module once a paid API tier is available
- [ ] Add an Nmap module for the active-recon phase (separate from this passive-only tool, but designed to feed the same report format)
- [ ] Add GVM/OpenVAS integration for vulnerability scanning on discovered live hosts
- [ ] HTML report export in addition to markdown
- [ ] Optional PDF export for client-ready deliverables

## Disclaimer

This tool is intended for authorized security research and reconnaissance on domains you own or have explicit permission to test. All checks are passive except for the httpx live-host probe (a single low-impact HTTP request per host, comparable to a normal page visit). Always confirm scope and authorization before running any reconnaissance activity against a third party.

---

*Built as part of an ongoing cybersecurity learning journey — see the [Cisco Ethical Hacker lab writeups](../penetration-testing/) in this repo for the manual, tool-by-tool version of these same techniques.*
