# Active Recon Lab: Enumeration with Nmap

This lab is where the Cisco Ethical Hacker course crosses a real line — everything up to this point (crt.sh, Shodan, breach lookups, Google dorking) was passive. Nothing touched the target. This one does. Nmap sends packets directly to a live host, which means it's the first lab in the series that would actually show up in someone's logs.

## The scenario

A Wireshark capture flagged unusual activity on a machine sitting on a lab DMZ network (10.6.6.0/24). The task: use Nmap to find out what that host is running and whether anything about it looks like a security problem. Straightforward incident-response framing — a host looked suspicious, and the job is figuring out why before deciding what to do about it.

## Part 1: Getting familiar with Nmap

Before running anything against the target, the lab walks through Nmap's core scan types via `man nmap`. Worth having these memorized rather than looked up every time:

| Option | What it does |
|---|---|
| `-A` | Aggressive scan — OS detection, version detection, script scanning, and traceroute all in one |
| `-O` | OS detection only |
| `-p <ports>` | Scan specific ports or port ranges |
| `-sF` | TCP FIN scan — a stealthier alternative to a full connect scan |
| `-sn` | Host discovery only — no port scan, just "is this alive" |
| `-sS` | TCP SYN scan — the classic "half-open" stealth scan |
| `-sT` | TCP Connect scan — completes the full handshake, noisier but doesn't need elevated privileges |
| `-sV` | Probes open ports to identify service and version |
| `-T<0-5>` | Timing template — higher numbers scan faster but are easier to detect |
| `-v` | Verbose output |
| `--open` | Only show ports that are open (or possibly open) |

The `-A` flag deserves a specific callout: it's genuinely useful because it bundles OS detection, version detection, and scripting into one command, but it's also loud. Any IDS worth deploying will flag it. Permission before running it outside a lab isn't optional.

## Part 2: Scanning the DMZ

### Step 1: Find what's alive

A host discovery scan (`-sn`) is the quiet first move — no port scanning yet, just checking who's home:

```
nmap -sn 10.6.6.0/24
```

This works by sending an ICMP echo request, a TCP SYN to port 443, a TCP ACK to port 80, and an ICMP timestamp request — any single response back confirms the host is up. Six active hosts turned up on this network, Kali included.

### Step 2: Scan the suspicious host

With the flagged IP identified, a default scan runs against it directly:

```
nmap 10.6.6.23
```

Six open ports came back: **21, 22, 53, 80, 139, 445**. That's FTP, SSH, DNS, HTTP, and the two classic SMB ports — enough of a spread to be worth digging into individually.

Worth understanding what the default scan is actually doing underneath: it's a TCP connect scan (`-sT`) against the 1,000 most common ports, completing the full TCP handshake for each one. That's effective, but it's also the noisiest option — every completed connection is a clear signature for anything watching the network. The three-way response table matters here too: **SYN-ACK means open**, **RST means closed**, and **no response (or an ICMP unreachable) usually means a firewall is filtering that port** rather than the service being absent.

### Step 3: OS detection

```
sudo nmap -O 10.6.6.23
```

`-O` needs elevated privileges since it relies on analyzing subtle differences in how a TCP/IP stack responds — the result came back as Linux, kernel range 4.15–5.8. Not a specific distro, but enough to start narrowing exploitation research.

## Part 3: Digging into FTP

Port 21 warranted a closer look, combining verbosity, a specific port, version detection, and fast timing into one command:

```
nmap -v -p21 -sV -T4 10.6.6.23
```

That returned **vsftpd 3.0.3** — a specific, known FTP server version, which immediately matters because specific versions map to specific CVEs.

Pushing further with the full aggressive scan against just that port:

```
nmap -p21 -sV -A 10.6.6.23
```

The output confirmed something worse than an outdated version — **anonymous FTP login was allowed** (FTP response code 230), and once connected anonymously, four files were sitting there readable: three innocuous-looking text files, and one named in a way that made its contents obvious without opening it. That naming choice alone is a small, real lesson: a sensitive file sitting in a public, unauthenticated FTP directory doesn't need a clever exploit to be a problem. It just needs someone to look.

The bigger issue underneath all of it: the scan explicitly showed **control and data connections both running in plain text**. Even setting anonymous access aside, any legitimate credentials used against this FTP server would be trivially interceptable on the wire.

## Part 4: SMB enumeration

Ports 139 and 445 (NetBIOS/SMB) got the same aggressive treatment:

```
nmap -A -p139,445 10.6.6.23
```

This identified the host as running **Samba 4.9.5 on Debian**, sitting in the default `WORKGROUP` — and flagged something specific in the SMB security settings: **message signing was disabled**, explicitly called out in the scan output as "dangerous, but default." That phrasing is worth sitting with — this isn't a misconfiguration someone introduced by accident, it's the out-of-the-box setting on a lot of systems, which is exactly why SMB relay attacks remain a persistent, well-known issue.

### Enumerating usernames

Nmap's Scripting Engine (NSE) carries purpose-built scripts for exactly this kind of digging. `smb-enum-users.nse` attempts to pull valid account names directly off the target:

```
nmap --script smb-enum-users.nse -p139,445 10.6.6.23
```

Two usernames came back. That's a meaningful result on its own — usernames turn a brute-force attempt from "guess both fields" into "guess one field against a known-valid account," which is a substantially easier problem.

### Enumerating shares

```
nmap --script smb-enum-shares.nse -p445 10.6.6.23
```

This is where the lab's findings tip from "concerning" to "actually bad." Three shares turned up, two of them hidden (share names ending in `$`, which is the SMB convention for administrative/system shares not meant to appear in a normal browse list). Every single share — hidden or not — reported **anonymous access: READ/WRITE**.

That's the standout finding of the entire lab. Anonymous write access to what's described in the share comment as a confidential file directory means anyone who can reach this host on the network can read, modify, or drop files into it without ever authenticating. Combined with the earlier SMB signing gap, this is a host with almost no barrier between "on the network" and "has meaningful access to it."

## Reflection: what actually goes in the report

The lab closes by asking the obvious next question: if this were a real assessment, what makes the cut for the findings report? Pulling it together:

- Outdated/specific FTP version (vsftpd 3.0.3) with anonymous login enabled
- Plaintext FTP control and data channels
- A sensitive file sitting in a publicly readable directory
- SMB message signing disabled (default, but still a real exposure)
- Two enumerable usernames via NSE scripting
- Two hidden SMB shares plus one visible one, all three with anonymous READ/WRITE access

Every one of these was found using nothing but Nmap and its built-in scripts — no custom exploitation, no manual protocol work. That's really the throughline of this lab: enumeration alone, done properly, tells you almost everything about how exposed a host actually is before a single exploit gets attempted.

## Takeaway

This is also the lab that shows both sides of the same tool clearly. A network technician runs this exact sequence to inventory their own infrastructure and catch these misconfigurations before anyone else does. A malicious actor runs the identical commands to find precisely the same soft points. Nmap doesn't care which side of that line the operator is on — which is exactly why authorization has to be settled before any of this gets pointed at something that isn't yours to test.

---
*Lab source: Cisco Ethical Hacker course — "Enumeration with Nmap"*
