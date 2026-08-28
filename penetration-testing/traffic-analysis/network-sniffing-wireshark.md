# Passive Recon Lab: Network Sniffing with Wireshark

This lab pairs two tools that work well together: `tcpdump` to capture traffic quietly from the command line, and Wireshark to actually make sense of what got captured. The lab frames Wireshark specifically as a **passive** tool — it doesn't send anything onto the network, it just watches. That distinction matters a lot in a recon context, since passive collection is far harder to detect than anything that actively probes a target.

## Part 1: Preparing the host

Before capturing anything, the lab has you get familiar with the environment you're capturing on:

```
pwd
```
Confirms the working directory — where the capture file will land once saved.

```
ifconfig
```
Identifies the Ethernet interface (typically `eth0`) and records its IP and MAC address. This matters later — when analyzing captured packets, this becomes the reference point for confirming which traffic actually originated from this machine.

```
ip route
```
Shows the default gateway — the address that responds to ARP requests for anything outside the local subnet, and the address packets get routed through as their first hop off-network.

```
cat /etc/resolv.conf
```
Reveals the configured DNS server. This is the address every DNS query in the upcoming capture will be sent to, and the source address DNS replies will come back from — worth knowing ahead of time so it's recognizable in the packet list rather than just another unfamiliar IP.

## Part 2: Capturing traffic with tcpdump

With the environment mapped, the actual capture starts:

```
sudo tcpdump -i eth0 -s 0 -w packetdump.pcap
```

Breaking down what each flag is doing:
- **`-i eth0`** — capture only on this interface (omit it and tcpdump captures everything, on every interface, which gets noisy fast)
- **`-s 0`** — snapshot length set to the default full capture size (262144), meaning packets aren't truncated
- **`-w packetdump.pcap`** — write raw output to a `.pcap` file rather than printing to the terminal, so it can be opened later in Wireshark or any other packet analysis tool

With the capture running silently in the background, normal browsing generates the traffic worth analyzing: a visit to Google, then a login to Skills for All in a second tab. Nothing scripted or forced — just an ordinary couple of page loads, which is exactly the point. `Ctrl+C` stops the capture, and `ls packetdump.pcap` confirms the file landed where expected.

## Part 3: Reading the capture in Wireshark

```
wireshark
```
opens the GUI, and `File → Open` loads `packetdump.pcap`.

### Filtering for DNS

Typing `dns` into the filter bar strips a large, noisy capture down to just the domain lookups — immediately the most readable part of the whole file. Every time a browser needs to resolve a hostname to an IP, that request and its response show up here, back to back, timestamped.

What's genuinely interesting is what shows up beyond the one site actually typed into the address bar. A single page load triggers a surprising number of secondary DNS queries — social media platforms, analytics services, CDN and certificate-validation domains — all called quietly in the background just to render one page. The lab makes the point directly: **knowing what sites a target visits regularly is valuable information for building a convincing social engineering attempt**, and DNS traffic alone hands that over without needing anything more invasive.

Searching for a specific hostname (`netacad`, using the search icon with **String** selected) jumps straight to the relevant query. Expanding **Ethernet II** confirms the source MAC address matches the interface recorded back in Part 1 — a small but useful sanity check that ties the captured traffic back to the machine that generated it. Expanding the **Domain Name System (query)** section further, then following the link to its paired response, reveals the actual resolved IP addresses behind the domain.

### Analyzing an HTTP session

The second half of the lab moves from DNS to a full HTTP interaction, this time against a DVWA (Damn Vulnerable Web Application) instance running locally in a Docker container. First step is identifying which interface is on the relevant subnet — `ifconfig` again, looking for the bridge interface tied to that network — and starting a fresh Wireshark capture on that specific interface rather than the general Ethernet one.

With the capture running, logging into DVWA over plain HTTP (not HTTPS) and searching the capture for `POST` finds the exact packet carrying the login request. Expanding **HTML Form URL Encoded** reveals the submitted username, password, and an accompanying user token — all sitting in cleartext, fully visible to anyone who captured this traffic. That's the practical, uncomfortable core of this half of the lab: **HTTP transmits form data with zero protection**, and a login form is exactly the kind of data nobody wants exposed that way.

Searching further for `302 Found` locates the server's redirect response following a successful login, and expanding it reveals a `Set-Cookie` header assigning a `PHPSESSID` value — the session identifier the server will use to recognize this user on future requests. Following the very next `GET` request from the client shows that same `PHPSESSID` being sent right back to the server in a `Cookie` header, confirming the session handoff worked as expected — and confirming, just as clearly, that anyone who captured that cookie value could potentially reuse it to hijack the session without ever needing the original password.

## Why this matters

The lab's own reflection question gets at the real value here directly: packet capture lets someone monitor and collect traffic **without ever being detected**, since nothing is actively sent to the target — it's pure observation. Captures can be saved and picked apart at leisure, long after the actual traffic happened. And what comes out of a capture like this is substantial: IP addresses, MAC addresses, DNS servers, visited sites, session cookies, and — when a target is still running plaintext HTTP — login credentials in the clear.

## Takeaway

This lab is a clean illustration of why HTTPS-everywhere matters as a baseline, not a nice-to-have. Every DNS query in this capture was visible regardless of encryption, which is expected and mostly unavoidable — DNS itself is typically unencrypted by default. But the DVWA login was fully exposed purely because the site never upgraded past plain HTTP — no exploit, no clever technique, just a protocol choice that handed over a username, a password, and a working session cookie to anyone quietly capturing traffic on the same segment. Passive collection doesn't announce itself, doesn't touch the target, and often doesn't need to work very hard at all to be worth the effort.

---
*Lab source: Cisco Ethical Hacker course — "Network Sniffing with Wireshark"*
