# Brief Report

**Give a topic. Get a finished market brief back.**

Most briefing tools sell you raw headlines and leave the synthesis to you. This Actor sells the *finished brief*: one run researches one topic live and returns a single structured result:

- **News signals** — the topic's current notable developments, each with its source URL
- **Trend momentum** — search-interest trend, rising queries and regional interest for the topic
- **Headline sentiment** — scored sentiment with the bull/bear drivers behind it

## Input

| Field | Required | Description |
|---|---|---|
| `topic` | Yes | Topic to brief, e.g. `Vietnam pangasius exports` |

## Output

One dataset item per run containing the full brief: `news`, `trends`, `sentiment`, plus `generated_at` and any `partial_failures` (the brief reports honestly if one component could not complete).

## Pricing

Pay per event: **one charge per completed brief** ($0.29). If the brief fails, the run fails and you are not charged for a result you did not get.

## Who runs this

Operated by **Mekong Trade Intelligence**, a pay-per-call API seller on Base (x402). The same brief is available directly as an API for agent builders; this Actor is the no-wallet, no-crypto way to buy it.

Results are generated live for each run from current web sources — they are research assistance, not financial advice.
