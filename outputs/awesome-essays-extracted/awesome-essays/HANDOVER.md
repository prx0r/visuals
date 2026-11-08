# Handover — all repos & services (2026-09-26)

## Running services (systemd --user, this box)

- pow-site (127.0.0.1:8795) → public via Cloudflare tunnel
  `powpowpow-box` → https://crypto.pow.systems (PUBLIC, token gate
  REMOVED by merge af3c7f6 — access.html login instead)
- pow-chain-state, pow-venue-l2, pow-venue-ws, pow-safetrade-l2 (STALE 57h+)
- pow-qubic-epoch (10min), pow-qubic-computors (hourly), pow-burn-snapshot (hourly, NEW)
- Timers: daily-state, signals, factors, analytics, provenance, r2-upload (R2 FAILED — backup unverified)

## What I built (all committed)

- powpowpow: Qubic burn fix 78.75→77.5% max, XMR 432, BTC hashprice units,
  per-computor mineable math, dead-script quarantine, dashboard token-join +
  price-format fixes, OPS panel rewrite, offline-analyst chat,
  burn_snapshot collector + /api/burns, qubicex/ content set (01–06)
- Merged origin ff3d952 (other agent: R2, SafeTrade, public dashboard).
  Pushed through 6890454 (handover snapshot).
- qubict (/home/box/qubict): SOURCES, TRANSFORMS, puell + ribbons + tests.
- powvid (/home/box/powvid): scaffold + epoch recap storyboard + test.
  NOT on GitHub (no remote yet).
- etsysignal: roastpet/pog.py (avatar+situations pipeline, verified PNGs),
  roastpet/meshy.py (brick API client), docs (ACTION_LIBRARY, SIGNATURE_
  PRODUCTS, BWIZARDS_COLLECTION). Check git state before touching.
- bwick: reviewed only (docs repo, memorial contradiction open).
- qubict/powvid/etysignal remotes: local-only unless stated.

## Secrets — ROTATE ALL (exposed in chat)

- GitHub classic token (ghp_…) — used for pushes, revoke now, use
  `gh auth login` going forward.
- Cloudflare API token (cfat_…) — used once for DNS, rotate.
- R2 S3 keys — never used, rotate anyway (were pasted in chat).
- Dashboard token in site.env + journal logs — rotate via site.env.

## Open threads (priority order)

1. SafeTrade WS stale 57h+ (was other agent's lane; now mine).
2. burn_ledger Query-API collector (BURNING events) — spec in
   qubicex/06; burn_snapshot (stats API) is live, this is the deep layer.
3. Verify viral -1.35T/week thread: tx-burn 225B/d CONTESTED (qubic.lt
   shows ~40B/d); denominator resolved (~177T circ).
4. Live BTC prediction via oracle — thesis-test catalyst, watch for numbers.
5. Tokenomics $1M buy+burn pilot — watch for uptake.
6. powvid push to GitHub (needs auth). qubict push (needs auth).
7. etsysignal: Meshy key → Buster brick test; ornament listing copy.
8. R2 backup still failed/unverified. Tunnel flaky on IPv6 (box egress).

## Key docs

- powpowpow/qubicex/01–06 (solutions, phases, explorer, scorecard,
  bull/bear + Sep addendum, burn pipeline spec)
- /home/box/content/docs/qubic-*.md (all-hands notes, founder, endgame, ARC)
- bwick/docs (plan repo — memorial posture UNRESOLVED across docs)
- This box: no GPU, 3GB RAM. No local ML. Venv at powpowpow/.venv (no pytest!).

## User context (do not trade on this, do respect it)

- Small layered QUBIC position, ladder bids below. Targets discussed:
  $500M base / $2B bull / $5B dream. Invalidation: flat ARC 2 quarters +
  dead prediction task + no pilot uptake + worsening burden.
- Prefers speed, hates process. Decisions live in chat; docs record them.
