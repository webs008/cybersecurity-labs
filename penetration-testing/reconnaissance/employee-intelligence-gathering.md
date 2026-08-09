# Recon Lab: Employee Intelligence Gathering

This lab flips the usual recon target around — instead of a company, you go after yourself. The exercise is to put on a threat actor's hat and see exactly how much personally identifiable information (PII) you can pull together using nothing but public search engines and social media. It's uncomfortable in a useful way. Most people assume they're not exposing much until they actually go look.

A quick note on scope before diving in: this kind of investigation is only fair game on your own accounts, or on someone else's with their explicit permission. Poking around someone's social presence without consent isn't a gray area — depending on where you are, it can cross into legal territory fast.

## Part 1: Gathering information through social media

### Step 1: Search for yourself

Start with a plain search-engine pass — your name, your usernames, name variations (maiden name, middle initial, married name, whatever applies). Do this in a private/incognito window. Otherwise your saved logins and search history quietly bias the results, and you won't get an honest read on what's actually indexed and publicly visible.

### Step 2: Audit yourself like a stranger would

This is the part that actually stings a little. Set up a throwaway social account and look at your own profiles the way someone with zero context on you would see them. Go through every platform you've ever used, not just the ones you're active on now.

What you're looking for isn't one big secret — it's the accumulation of small, ordinary details that build a profile:

- **Profile basics** — full name, birthdate, contact info
- **Status updates** — life events, relationship and employment status, political or religious opinions
- **Location data** — hometown, geo-tagged check-ins
- **Shared content** — photos and comments you've posted, plus anything you're tagged in
- **Friends and family posts** — information about you that other people put online, which you don't control at all
- **Public discussions** — forums, comment threads, anywhere you've weighed in under your real identity

None of these individually feel dangerous. Put together, they're a fairly complete profile of where you work, where you live, what your routine looks like, when you're away from home, and who your close contacts are. That's the part that's easy to miss when you're posting one thing at a time — nobody sits down and deliberately builds the profile, it just accumulates.

## Part 2: What an attacker actually does with this

It's one thing to find the information. It's another to think through how it gets weaponized.

**Workplace information** is the most immediately dangerous piece. Once an attacker knows where you work and who you report to, they've got everything needed for a targeted phishing or whaling attempt — an email that looks like it came from your actual manager, referencing your actual team, sent at a moment that looks routine.

**Hobbies and interests** open a softer angle. A fake landing page built around something you're genuinely into is far more convincing than a generic phishing template — it's the difference between an obvious scam email and one that feels tailored, because it is.

**Public conversations with friends and family** are the quiet one. People drop real clues in casual conversation without noticing — a pet's name, a childhood street, an old school. Those aren't idle chat to an attacker; they're security-question answers sitting in plain sight.

## Best practices that came out of this

A few habits actually make a measurable difference:

- Don't post in real time — a delay of even a few hours means your location data isn't live
- Lock down social accounts to private wherever the platform allows it
- Pause before sharing anything that reveals a pattern (routine, schedule, location) rather than a one-off moment
- Treat any request for sensitive details or payment info as suspicious by default, especially if it references something you posted publicly

## Takeaway

The uncomfortable part of this lab isn't the tooling — there isn't any, really, just search engines and a spare hour. It's realizing how much of a profile builds itself from things that felt harmless to post one at a time. Nobody sits down and thinks "I'll expose my employer, my routine, and my family's names to strangers" — it happens a photo and a comment and a check-in at a time, and by the time you audit it as a stranger, it adds up to more than most people would ever hand over on purpose.

---
*Lab source: Cisco Ethical Hacker course — "Employee Intelligence Gathering"*
