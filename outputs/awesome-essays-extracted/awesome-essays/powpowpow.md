# PowPowPow — Vision & Architecture

## The Thesis

**PowPowPow = data/research infrastructure for weird compute-heavy crypto.**

Content is distribution for the data layer, not the product itself.

The moat is the normalized dataset. For every chain you track, collect the same canonical fields. Then derive metrics nobody else publishes.

---

## Surfaces

- **powpowpow.dev** — API, docs, schemas, developer tooling
- **powpowpow.info** — public dashboards, explainers, chain profiles, live metrics
- **PowPowPow** — YouTube/social identity
- Later: premium feed/API for traders, miners, researchers, agents

---

## The Flywheel

```
API/data collection → anomaly → research → video/article → audience feedback → new metric request → better API → more anomalies
```

YouTube titles become naturally data-driven:
- "Pearl miners are creating $1M/day — who is buying it?"
- "Qubic's real inflation rate after the halving"
- "Which AI mining networks actually produce useful compute?"
- "What happens to Monero if AGI makes software free?"
- "Nockchain vs Qubic: what is the network actually paying for?"
- "The weirdest coins on SafeTrade ranked by miner economics"

---

## First Dataset: SafeTrade L2 Universe

### Tier 1 (Anchor)
| Coin | SafeTrade Volume | Why |
|------|------------------|-----|
| **QUBIC** | ~$21.6k/day | Anchor. Unusual emission/burn. L2 data useful. |
| **PRL** | ~$3.1M/day | Contrast case. Heavy miner issuance. Useful-compute narrative. |
| **NOCK** | ~$159k/day | Differentiated proof/computation thesis. |
| **QUAN** | ~$129k/day | Newly listed. Post-quantum PoW. Privacy. ZK. |
| **TSC** | ~$41k/day | Useful-AI-inference mining. |
| **GNK** | ~$21k/day | Compute-market experiment. |
| **XMR** | ~$6.8k/day | Mature PoW/privacy benchmark. Connects to XMRBot. |

### Tier 2 (Second Wave)
| Coin | SafeTrade Volume | Notes |
|------|------------------|-------|
| **NPT** | ~$2.1k/day | Private-by-default STARKs. |
| **XTM** | ~$2.6k/day | Mimblewimble. RandomX. |
| **XEL** | ~$41/day | BlockDAG + privacy. Tiny. |

---

## Canonical Fields Per Chain

### Market Data
- Price, circulating/max supply, FDV
- Exchange liquidity (SafeTrade depth, spread)
- Volume (24h, 7d)

### Mining/Economics
- Issuance/day, issuance USD/day
- Block reward, block time
- Hashrate, difficulty
- Miner revenue, estimated mining cost
- Profitability by hardware (GPU/CPU/ASIC)
- Pool concentration (top pools / total hashrate)

### Derived Metrics (The Moat)
- **Miner sell burden** = new issuance × estimated miner sell fraction
- **Absorption ratio** = spot volume / new issuance value
- **Dilution pressure** = annualized issuance / circulating cap
- **Compute efficiency** = useful compute value / miner subsidy
- **Narrative premium** = FDV relative to actual usage/compute
- **Security spend** = miner rewards / economic activity

### L2/Order Book (Real-time Only)
- Spread
- Depth at ±0.5/1/2/5%
- Replenishment rate
- Order cancellations
- Signed trade flow
- Aggressive buy/sell imbalance
- Realized slippage
- Book asymmetry
- Whale-size resting orders
- Liquidity response after block rewards hit miner wallets

### Chain Metrics
- Active addresses, transactions
- GitHub activity
- Actual useful-compute output (where relevant)
- Major protocol events (epochs, halvings, burns)

---

## Causal Chain (Backtestable)

```
emission → miner payouts → exchange inflows → L2 sell pressure → price impact
```

### Testable Hypotheses
1. **PRL**: Spikes in newly distributed miner rewards predict increased ask depth or negative returns 1h/6h/24h later
2. **QUBIC**: Epoch boundaries, burns, mining profitability, hashrate, or Aigarth events predict order-flow imbalance
3. **NOCK**: ZK-proof generation activity correlates with network security spend
4. **TSC**: Inference demand spikes predict miner revenue changes

---

## Automated Mining Layer

**PowPowPow = profitability/control layer for mining.**

Given: hardware model + electricity cost + pool fees + chain difficulty + token price

Answer: `What should this GPU mine right now?`

Eventually: `mine → receive rewards → hold/swap according to policy`

Connects to XMRBot infrastructure. XMR = natural settlement/privacy rail.

### API Endpoints (Later)
- `/profitability` — what to mine right now
- `/miners` — hardware fleet status
- `/markets` — SafeTrade pair data
- `/orderbooks` — L2 depth
- `/emissions` — chain issuance data
- `/flows` — miner wallet tracking
- `/swap-routes` — automated conversion paths

---

## Content Category

**Weird systems that remain valuable when software/intelligence becomes cheap.**

Includes:
- XMR (privacy/money)
- Qubic (useful PoW)
- TAO (machine intelligence incentives)
- Nockchain (ZK-PoW)
- Zcash (privacy)
- Decentralized compute
- Verifiable inference
- Post-quantum crypto
- Mining economics
- Privacy infrastructure

---

## First Milestone

**Archive every SafeTrade L2 update + trades for the seven Tier 1 coins, then normalize chain issuance/mining metrics into the same timestamped schema.**

30-90 days of data → genuinely interesting strategies.

---

## Three Activities Reinforce Each Other

```
data/API → trading signals → mining optimization → content
```

Content produces hypotheses you can test against the data rather than becoming empty commentary.

---

## Current Infrastructure (This Repo)

```
safetrade/
├── multi_coin_collector.py    — WebSocket L2 collector
├── tracked/                   — Real-time L2 + historical OHLCV
├── qubic_historical_data.json — QUBIC OHLCV
├── .env                       — API credentials
└── venv/                      — Python environment
```

### Tracked Coins
QUBIC, NOCK, GNK, TSC, PRL, NPT, QTC, XEL, XTM, XMR

### Data Sources
- **SafeTrade WebSocket** — Real-time L2 depth + trades (10 coins)
- **MEXC** — Historical OHLCV (5 coins: QUBIC, NOCK, PRL, XEL, XTM)
- **Bitget** — Historical OHLCV (QUBIC, PRL)
