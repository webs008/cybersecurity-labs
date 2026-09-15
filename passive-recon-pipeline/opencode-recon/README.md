# AI-Assisted Recon Comparison Workflow

An experiment in using an AI coding agent ([OpenCode](https://opencode.ai)) alongside a manual bug bounty recon methodology — running on free models first, with the goal of comparing tool choices and technique rather than replacing manual work outright.

## Motivation

Recon tooling (this repo's `passive-recon-pipeline` included) encodes a fixed methodology: a specific set of tools, run in a specific order, looking for specific things. That methodology was built by hand, iteratively, based on what worked.

This workflow asks a different question: **what would an AI agent do differently, given the same target and no prior instructions beyond "do recon"?** Where it reaches for a tool or technique this pipeline doesn't already use, that's a candidate for a new module. Where it misses something the pipeline already catches, that's a data point too — it doesn't mean the AI is wrong, just that the comparison is informative either way.

The explicit rule for this workflow: **start on free models, only pay if the free tier stops surfacing anything the manual process doesn't already catch.**

## Architecture

```
opencode-recon/
├── Dockerfile              # Node + recon toolchain (curl, whois, dnsutils, nmap)
├── config/
│   └── opencode.json       # OpenRouter provider config, free-tier models
├── workspace/
│   ├── scope.md            # Per-target scope, in/out-of-scope, program rules
│   └── session.log         # AI recon transcript, saved per run
├── auth/                   # Persisted OpenRouter credentials (gitignored)
└── .env                    # OPENROUTER_API_KEY (gitignored)
```

The agent runs in a container, isolated from the host, with recon tools installed so it has something to actually invoke when it decides to enumerate DNS, check WHOIS, etc.

## Setup

```bash
# Build the image
docker build -t opencode-recon .

# Run with the OpenRouter key injected as an env var
docker run -it --rm \
  --env-file ~/opencode-recon/.env \
  -v ~/opencode-recon/workspace:/workspace \
  -v ~/opencode-recon/config:/root/.config/opencode \
  -v ~/opencode-recon/auth:/root/.local/share/opencode \
  --name opencode-recon-session \
  opencode-recon \
  opencode
```

`config/opencode.json` points at OpenRouter's free-tier router (`openrouter/free`), which auto-selects whichever free model is currently live — avoiding the churn of hardcoded model IDs that OpenRouter periodically retires.

**Key config detail:** the `apiKey` option must explicitly reference the env var —
```json
"options": { "apiKey": "{env:OPENROUTER_API_KEY}" }
```
A custom provider block does not automatically inherit `OPENROUTER_API_KEY` from the environment; without this line, requests fail with a `Missing Authentication header` error even when the variable is set.

## Workflow loop

1. **Define scope** — write `workspace/scope.md` with target, in-scope domains, program rules, and anything already found manually.
2. **Run AI recon** — prompt OpenCode to read the scope file and do passive recon, narrating every tool it uses and why.
3. **Run the manual pipeline in parallel** — `passive-recon-pipeline`'s `recon.py` against the same target, same day.
4. **Diff the two** — log what each found and *how* it got there, not just the results.
5. **Close the gap** — feed genuine gaps back to the agent ("research current methodology for X, propose how to incorporate it"), and fold anything worth keeping into the manual pipeline as a new module.
6. **Repeat per bug class** — recon → auth/session → IDOR → SSRF → XSS → business logic, one methodology log per class.

## Comparison log template

| Target | Date | Tool/technique | Found by AI | Found manually | Notes |
|---|---|---|---|---|---|
| example.com | 2026-09-15 | Subdomain enum via crt.sh | ✅ | ✅ | Same result, AI also cross-checked via DNS zone transfer attempt |
| example.com | 2026-09-15 | JS file secret scanning | ✅ | ❌ | New — worth adding as a pipeline module |

## Troubleshooting notes (from setup)

- **Docker "Conflict: name already in use"** — a stopped container still holds the name; `docker rm <name>` before re-running, or add `--rm` so containers self-clean on exit.
- **"Permission denied" reading mounted files from host** — containers run as root by default, so files they create are root-owned on the host too; `sudo chown -R $(whoami):$(whoami) <path>` fixes it, or avoid `--user` overrides unless you also relocate config paths out of `/root`.
- **"Missing Authentication header" from OpenRouter** — almost always means the API key isn't reaching the request, either because `auth.json` persistence is unreliable across container restarts, or because a custom provider config needs an explicit `{env:VAR}` reference rather than relying on ambient environment inheritance.

## Status

- [x] OpenCode running in Docker against OpenRouter free-tier models
- [ ] First real comparison run against a live scope
- [ ] First methodology gap identified and folded into `passive-recon-pipeline`
- [ ] Repeat for auth/session bug class
- [ ] Repeat for IDOR
- [ ] Repeat for SSRF / XSS / business logic

## Related

- [`passive-recon-pipeline`](../) — the manual recon CLI this workflow is benchmarked against
