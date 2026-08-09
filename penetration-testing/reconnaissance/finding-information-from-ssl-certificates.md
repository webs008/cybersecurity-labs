# Recon Lab: Finding Information from SSL Certificates

Another one from the Cisco Ethical Hacker track. This lab is about something most people never think twice about — the little padlock icon in the browser bar — and how much recon value is sitting behind it. SSL/TLS certificates exist to prove domain ownership and encrypt traffic, but along the way they leak a surprising amount about an organization's infrastructure: subdomains, issuing authority, expiration dates, encryption algorithms, sometimes entire slices of attack surface nobody meant to expose.

## Part 1: Certificate info straight from the browser

Every site with HTTPS is showing you a certificate whether you look or not. Click the padlock next to the URL and you can dig into the details.

For `netacad.com` (Cisco's Skills for All platform), the certificate turned up some things I wasn't expecting:

- **Issued to:** `socialgoodplatform.com`
- **Issued by:** IdenTrust
- **Expiration:** January 6, 2024
- **Signature algorithm:** SHA-256 with RSA

That first line is the interesting part. The Skills for All site is actually running on a certificate issued to a completely different domain, `socialgoodplatform.com`. That's not a red flag by itself — organizations share certs across related properties all the time — but it's exactly the kind of connection an attacker (or a pentester) wants to know about. One domain quietly points you to another.

Certificates aren't just sitting in the browser either. Windows keeps them in `certmgr.msc`, and on Kali you'll find the trusted root certs under `/usr/share/ca-certificates/mozilla`. A quick way to isolate the root CAs there:

```
ls -l | grep root
```

Worth a mention: basic single-domain SSL certs aren't free from every provider. GlobalSign runs around $249/year, DigiCert about $274, and GoDaddy splits the difference — $99 self-managed, $250 if you want them managing it.

## Part 2: Certificate Transparency logs

This is where the lab actually gets interesting. Certificate Transparency (CT) is a public logging requirement — every certificate authority has to log every certificate it issues, publicly and permanently. It exists so anyone can audit whether a cert was issued fraudulently. Great for security. Also a goldmine for recon, because it means every subdomain that ever got a cert is sitting in a searchable public log.

[crt.sh](https://crt.sh) is the main interface for this. Search a domain and it pulls every certificate on record — going back years in this case, to 2019 for netacad.com.

Running `netacad.com` through it surfaced subdomains that a normal user browsing the site would never see — names starting with `dev` and `stage`. That naming convention gives it away: these are almost certainly internal environments used by the development team, not meant for public traffic at all. Finding a dev or staging subdomain during recon matters because those environments tend to run with weaker hardening than production.

crt.sh also confirmed the connection spotted earlier — `socialgoodplatform.com` shows up as directly tied to the netacad.com certificate chain. Searching that domain on its own turned up a much larger set of subdomains than Skills for All alone accounts for. That's the real signal here: the visible site is a small piece of a much bigger network, and CT logs are what expose the rest of it.

## Part 3: SSL tools that ship with Kali

Kali comes with a handful of SSL-focused tools out of the box. Worth knowing what each one actually does before reaching for it:

| Tool | What it does | Category |
|---|---|---|
| `sslscan` | Queries a server to see which ciphers it supports | Recon |
| `ssldump` | Captures and decodes SSL/TLS traffic | Exploitation |
| `sslh` | Lets multiple services share port 443 | Utility |
| `sslsplit` | Enables MitM attacks against SSL-encrypted connections | Exploitation |
| `sslyze` | Connects to a server and analyzes its SSL configuration | Recon |

`sslscan` and `sslyze` are the ones you reach for during recon — they tell you what's exposed without touching anything. `ssldump` and `sslsplit` are further along the chain, useful once you're actively intercepting traffic rather than just mapping it.

## Part 4: Running sslscan and saving readable output

`sslscan` is a solid starting point for checking what a target domain actually supports, cipher-wise. Straight from the terminal:

```
sslscan netacad.com
```

The output is color-coded, and the colors aren't decorative — they're a quick severity read:

- **Red background** — no encryption at all (NULL cipher)
- **Red text** — a broken cipher (≤40-bit) or an outdated protocol like SSLv2/SSLv3, or a weak signing algorithm like MD5
- **Yellow** — a weak cipher (≤56-bit) or SHA-1 signing
- **Purple** — an anonymous cipher (ADH/AECDH), meaning no real authentication is happening

That color coding is genuinely useful in a terminal, but it disappears the moment you try to save the output to a plain text file. That's where `aha` comes in — it converts terminal output (color included) into a real HTML file.

```
sudo apt update
sudo apt install -y aha
```

Then pipe `sslscan` straight into it:

```
sslscan netacad.com | aha > sfa_cert.html
```

Open the resulting file in Firefox and you get the same color-coded readout as the terminal, just on a white background and easy to archive or hand off in a report.

## Takeaway

Out of everything in this lab, crt.sh did the most work with the least effort. sslscan and sslyze tell you about the state of a single certificate — algorithm, expiration, cipher support. crt.sh tells you about the shape of an entire network: every subdomain that's ever had a certificate issued to it, including the ones nobody intended to advertise. For OSINT-style recon, that's the difference between checking a lock and finding out how many doors there actually are.

---
*Lab source: Cisco Ethical Hacker course — "Finding Information from SSL Certificates"*
