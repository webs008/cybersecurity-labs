# Recon Lab: Finding Out About the Organization

This one's from the Cisco Ethical Hacker track, and it's less about tools and more about a mindset shift: before you touch a target's network, you go find out everything you can about it from the outside. No exploits, no scanning the perimeter — just email breach lookups and file metadata. It's the kind of work that feels almost boring until you realize how much it actually hands you.

## The setup

Kali VM, internet access, and two things to go dig up:

1. Whether known email addresses show up in past breaches
2. What's hiding in the metadata of publicly posted files

Both fall under passive recon — you're not touching the target's infrastructure, just pulling on threads that are already public.

## Part 1: Email breaches

The idea here is simple. If a company's employees have had their work email reused across other breached services, there's a decent chance some of those passwords still work somewhere. Sites like Have I Been Pwned, F-Secure, HackNotice, BreachDirectory, and KeeperSecurity all let you search an address or a whole domain and see what turns up.

I ran a few addresses through these to get a feel for it. The interesting part isn't really the tool — it's what a "yes" means for a pentest. A breached email doesn't just confirm someone's account was compromised somewhere; it can hand you usernames, old passwords, and password patterns that are genuinely useful once you get to the exploitation phase. And a lot of organizations have no idea any of this happened until someone tells them.

### EmailHarvester

Next tool up: EmailHarvester, which pulls email addresses tied to a domain. It's not preinstalled on Kali, so first run prompts you to install it.

```
emailharvester -h
```

The flag that matters most here is `-d`, which points the tool at a target domain. I ran it against a few test domains — `h4cker.org`, `hackxor.net`, `scanme.nmap.org` — and it comes back with a list of addresses tied to that domain.

```
emailharvester -d h4cker.org
```

From there you can feed those addresses back into the breach-lookup sites from Part 1. If a chunk of a company's staff have credentials floating around from old breaches, that's a real attack surface — and it's one you found without sending a single packet at their network. You can also dump the results to a file with `-s`, which gets you an XML and text output that other tools can chew on later.

### Spiderfoot

Spiderfoot takes this further — it's an OSINT automation framework that runs a pile of modules against a target and correlates whatever it finds.

```
spiderfoot -l 127.0.0.1:5001
```

That spins up a local web GUI. From the Settings page you can browse the available modules — some need API keys, some don't. A few worth calling out for email-focused recon:

- **Leak-Lookup / Dehashed** — breach and leak databases
- **AccountFinder** — checks whether an address is registered on social platforms, code repos, forums
- **Archive.org / CommonCrawl** — historical snapshots of pages, which sometimes surface old contact info nobody bothered to scrub
- **Bing / DuckDuckGo** — straightforward search-engine correlation
- **EmailCrawlr / Ahmia** — more specialized crawling, including dark web indexing

You pick your modules under **New Scan > By Module**, name the scan, point it at a target, and hit **Run Scan Now**. What you get back is essentially a map of everywhere that email address has left a trace online — which is a lot more than most people expect.

## Part 2: File metadata

This half of the lab is about a mistake almost every organization makes at some point: posting a file publicly without stripping what's baked into it. A PDF report, a scanned document, a photo from a company event — all of it can carry metadata like the author's name, the software and OS used to create it, GPS coordinates, or internal usernames.

The tool for this is **ExifTool**, which reads metadata across a huge range of file types and is scriptable enough to run against an entire directory at once. It ships as a GUI too, for Windows/macOS/Linux, but the CLI is what you actually want for recon work.

Installing it on Kali:

```
sudo apt install libimage-exiftool-perl
```

`exiftool -list` shows every tag it knows how to read, and `exiftool -listf` shows the file types it supports. Broken down roughly by category:

| Type | Formats |
|---|---|
| Documents | PDF, TXT, DOC, DOCM, DOCX, HTML |
| Audio | FLAC, MP3, WAV, AIFF, RA, WMA |
| Video | AVI, DV, FLV, MOV, QT, MP4, MPEG, RM, WEBM, WMV |
| Graphics | BMP, EXIF, GIF, JPEG, JPG, PNG, SVG, TIFF |
| Archives | GZ, GZIP, RAR, ZIP |

For actual files to test against, the lab points you at the Google Hacking Database (GHDB) — dorks that surface publicly indexed files of a given type. Pull down a batch, point ExifTool at them:

```
exiftool /path/to/file
```

or against a whole folder at once, with the results exported to CSV:

```
exiftool -csv > /path/to/out.csv /path/to/folder
```

What comes back varies a lot by file, but it's often more than you'd expect — author names, internal usernames, device models, sometimes even GPS coordinates if the file came off a phone. One tag worth knowing: `CREATOR: gd-jpeg v1.0` means the image was generated by version 1.0 of the PHP GD library, which is old enough that it's worth checking for known vulnerabilities tied to that specific version.

## Takeaway

None of this required touching the target's network. No scans, no exploits, nothing that would trip an IDS. Just public breach data and metadata nobody thought to strip. That's really the point of this lab — reconnaissance isn't always about clever tooling, it's about being patient enough to pull every public thread before you ever get to the technical part of the test.

It's also hit-or-miss in a way active scanning usually isn't. Sometimes a domain search turns up nothing useful. Sometimes one photo's metadata hands you a device model and an internal username in the same breath. You don't know which until you look — which is exactly why this step doesn't get skipped in a real engagement.

---
*Lab source: Cisco Ethical Hacker course — "Finding Out About the Organization"*
