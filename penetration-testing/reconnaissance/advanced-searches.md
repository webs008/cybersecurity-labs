# Recon Lab: Advanced Searches

Another Cisco Ethical Hacker lab, and this one covers a technique that's almost deceptively simple: using Google itself as a recon tool. No scanners, no frameworks — just search operators and an archive of the entire internet. It's a good reminder that some of the most useful reconnaissance doesn't require anything more advanced than knowing how to ask the right question.

## Part 1: Google dorking

A plain search for "ethical hacker" pulls back an enormous number of results, and most of them are noise — maybe 10% actually relevant to whatever you're looking for. Google Advanced Search operators exist to cut that noise out, and once you start narrowing on purpose, the exercise stops being a search and starts being reconnaissance.

The operators used in this lab:

| Operator | What it does |
|---|---|
| `allintext:` | Restricts results to pages where all query words appear in the page text |
| `filetype:` | Restricts results to a specific file type (.pdf, .ppt, .doc, etc.) |
| `intitle:` | Restricts results to pages with a certain word in the title |
| `inurl:` | Restricts results to pages with a certain word in the URL |
| `site:` | Restricts results to a specific domain |

Syntax matters here — no space between the operator and the keyword. `site:pearson.com` works; `site: pearson.com` doesn't.

A few combinations from the lab, run against Pearson's domain:

```
ethical hacker site:pearson.com
```
Every result ties back to one domain — the entire result set is now scoped to a single organization.

```
ethical hacker site:pearson.com filetype:pdf
```
Same domain, but now filtered down to PDFs only — a fast way to surface reports, whitepapers, or internal documents that happen to be publicly indexed.

```
ethical hacker intitle:certification
```
Filters for a specific word appearing in the page title rather than just anywhere on the page — useful when you're hunting for a specific type of page (login portals, admin panels, certification pages) rather than a general topic.

This is the part that turns dorking from a curiosity into an actual recon technique: individually, each of these searches looks harmless. Stacked together against a real target, they start building a picture — what file types a company has exposed, what kind of pages exist on their domain, what employees are saying publicly. None of it required touching the target's infrastructure. It's all sitting in Google's index already.

### Turning it toward a real target

The lab has you pick an actual company and run the same operators against it, with one hard boundary stated up front: passive recon like this is legal, but acting on what you find — logging into an exposed admin panel, for instance — is not. If something genuinely concerning turns up, the right move is reporting it to the company, not exploiting it.

A few dorks worth running against any target domain:

```
site:examplecompany.com inurl:admin
```
Surfaces pages with "admin" somewhere in the URL — a first pass at finding admin panels or management interfaces that shouldn't be indexed at all.

```
site:examplecompany.com intitle:login
```
Finds login pages specifically — useful for mapping out what authentication surfaces exist and where.

```
site:examplecompany.com filetype:pdf
```
Pulls every indexed PDF on the domain — internal reports, policy documents, anything that got uploaded without much thought about who else could find it.

```
site:examplecompany.com intext:employee filetype:pdf
```
Stacks operators together — PDFs specifically containing the word "employee." This kind of combination search is where dorking earns its reputation; a single operator rarely finds much, but layering two or three narrows things down to exactly the kind of document that matters.

LinkedIn deserves its own mention here:

```
site:linkedin.com intitle:examplecompany
```
This one's less about files and more about people. It can surface employees, their roles, sometimes photos — and by extension, the technology stack a company uses, since people list their tools and skills on their own profiles without thinking twice about it. For a hacker building toward a social engineering attempt, this is often more valuable than any technical finding, because it hands over names, titles, and a sense of who to target.

## Part 2: The Google Hacking Database (GHDB)

Dorking gets a lot more efficient once you stop reinventing every query from scratch. The GHDB is a public, community-maintained index of pre-built dorks, organized by category — things like login pages, files with passwords, vulnerable servers, sensitive directories.

Each entry in the database includes:

- A GHDB-ID
- The author who submitted it
- The date it was published
- A short description of what the dork actually finds
- A clickable link that runs the dork immediately

Filtering by category and browsing is one way to explore it. Quick Search is faster if you already know what you're after — searching `tsweb`, for instance, surfaces a well-known dork targeting Remote Desktop and terminal services login pages. Clicking into results from that search can reveal more than just a login prompt — sometimes the version of the underlying OS running the service is visible right there on the page. Knowing a target is running an end-of-life OS like Windows 2000 immediately narrows down which known vulnerabilities are worth investigating.

Category filters stack with search terms too. Selecting **Files Containing Passwords** and searching `db_pass` returns dorks specifically aimed at exposed database credential files — a category of finding that, when it hits, tends to be far more serious than a stray PDF.

## Part 3: The Wayback Machine

This is the part of the lab that reframes recon as something that happens across time, not just against the live version of a site. The Wayback Machine (web.archive.org) crawls and archives the internet continuously, which means a target's current site is only one layer of what's actually available — older, less-secured versions of the same domain are sitting right there in the archive.

A few tabs worth knowing:

- **Calendar** — shows crawl frequency and lets you jump to a snapshot from a specific date, sometimes navigable as if the page were still live
- **Collections** — shows which archiving projects crawled the site and when
- **Changes** — highlights how much a page has shifted between two captures; grey means minimal change, blue means something significant happened
- **Summary** — a domain-wide view of content types (text, image, script, etc.) hosted over a chosen date range
- **Site Map** — a visual map of a domain's structure over time, root at the center, complexity radiating outward
- **URLs** — every URL ever archived under a domain, filterable by extension

That last one is where things get genuinely useful. Filtering for `.bak`, `.zip`, `.config`, `.csv`, or paths like `/admin/` and `/api/` can surface files that were never meant to stay public — configuration backups, old admin routes, data exports — long since removed from the live site but still sitting in an archived crawl.

The advantage for a hacker isn't just the information itself. It's that pulling data from an archive doesn't touch the target's live infrastructure at all, which means there's nothing to detect. Combine that with whatever historical context the archive reveals — old company details, past employees, previous technology choices — and you've got groundwork for a social engineering attempt that's genuinely hard to trace back to any reconnaissance activity at all.

## Takeaway

Nothing in this lab required a single piece of specialized tooling. A search engine and a public archive did all the work. That's really the throughline across every recon lab in this series: the barrier to finding meaningful information about a target is almost never technical. It's knowing where to look, and being patient enough to actually look there before moving on to anything more aggressive.

---
*Lab source: Cisco Ethical Hacker course — "Advanced Searches"*
