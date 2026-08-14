# Recon Lab: Shodan Searches

This one covers Shodan — a search engine that doesn't index web pages, it indexes devices. Webcams, routers, industrial control systems, smart appliances, anything sitting on the internet with an open port. Where Google crawls content, Shodan crawls infrastructure. And a lot of that infrastructure was never hardened by whoever installed it.

## What Shodan actually collects

Shodan's fundamental unit of data is the **banner** — the response a service gives back when something connects to it. Every open port has a banner, and those banners routinely leak far more than they should: software name, version number, sometimes default configuration details nobody bothered to change.

Setup is a free account plus an API key, though the free tier caps you at limited results per search and no filter access from the CLI. Enough to see how the tool works; a paid tier is what you'd want for anything resembling real engagement work.

## Searching the web interface

A plain search for `webcam` returns a results page with more context than expected — total device count, top countries, top organizations, top products, top operating systems, all summarized on the side. In this run, the US came back as the top country for exposed webcams by a wide margin.

Clicking into an individual result opens a detail page: approximate geographic location, hostnames, domain, country, city, organization, ISP, ASN, and — critically — every open port Shodan found on that device, along with headers, served pages, and certificate info for each one. On a typical webcam result, ports 8081, 8088, and 80 showed up consistently.

Worth flagging: not every device that shows up in a "webcam" search is actually a webcam. The word just needs to appear somewhere in the banner. Still, banners frequently name the actual manufacturer, and that's a real thread to pull — cross-reference a manufacturer name against known default credentials, and you've got a workable list of devices that may never have had their password changed since the day they were plugged in. (Worth saying plainly: looking this up is recon. Logging into a device you don't own or have permission to access is not, and crosses straight into illegal territory.)

## Filtering with search syntax

Shodan's filter syntax is `filter:value`, no space, quotes around anything with a space in it:

| Filter | What it does |
|---|---|
| `country:XX` | Two-letter country code |
| `city:city-name` | Search by city |
| `region:region-name` | Search by state or region |
| `product:product-name` | Search by specific product |
| `version:XX` | Search by product version |
| `vuln:XX` | Search by a specific CVE |

Stacking filters is where Shodan gets genuinely sharp. This search targets a known configuration weakness directly:

```
port:21 country:US region:CA city:"San Jose" 230
```

Port 21 is FTP, and `230` is the FTP success response code for a completed login. Combined, this query finds FTP servers in San Jose that are accepting anonymous logins — the response returned 847 matches at the time of testing. That's not a hypothetical vulnerability. That's 847 confirmed misconfigured servers sitting there, discoverable in a single search string.

Results can also carry `cloud` or `honeypot` labels. Clicking into a cloud-labeled result adds cloud provider, cloud region, and cloud service to the general info section — useful for mapping out which cloud infrastructure an organization is actually running on, beyond whatever they publicly disclose.

A product-specific search works the same way — `Apache port:80 city:"your-city"` narrows results down to Apache servers running in a specific location, which is a fast way to get a read on what software and versions are prevalent in a given area or organization.

## Using Shodan from the CLI

Shodan ships as a Python library, preinstalled on Kali. Initialize it with the API key from your account page:

```
shodan init <your API key>
```

A successful init returns "Successfully initialized." From there, the same searches run from the terminal:

```
shodan search webcam
```

Output comes back as unformatted text — IP, port, and device name for each match — which makes it straightforward to pipe into a script for automated searching. One limitation worth knowing: filter syntax isn't available on the free API tier from the CLI, only unfiltered search terms.

A few other CLI commands worth having in the toolkit:

- `shodan info` — shows remaining query and scan credits
- `shodan myip` — returns your own outbound IP, the one that would show up on the receiving end of any packets you send
- `shodan stats <query>` — pulls the same summary statistics the web interface shows, without the visual dashboard

## Why this matters beyond recon

Shodan's value cuts both ways. For an attacker, it's a shortcut past the scanning phase entirely — instead of scanning ranges yourself, you're querying a database that already scanned the whole internet for you. For defenders, it's the same data used in reverse: search your own organization's IP ranges, see exactly what Shodan sees, and fix what's leaking before someone else finds it first. Header information that shouldn't be public, outdated software versions tied to known CVEs, ports that were never meant to be internet-facing — all of it is visible from the same search bar.

## Takeaway

Shodan makes a point that's easy to underestimate: the internet already has an index of every insecure device connected to it, and it's searchable by anyone with a free account. 847 anonymous-login FTP servers in one city, found with one query, is a good reminder of just how much exposure exists simply because nobody went looking until now.

---
*Lab source: Cisco Ethical Hacker course — "Shodan Searches"*
