# EastAlmanac Tarot Reading (塔罗) — Data Layer

**塔罗** here is the classic **Rider-Waite-Smith (RWS 1909)** deck — 78 cards, 22 Major Arcana + 56 Minor (Wands/Cups/Swords/Pentacles × 14). The page draws deterministically from a seed (the reveal moment + the user's pick order); the returned payload carries the spread, each card's upright/reversed state, and a reproducible `/r/` link. Route here when the user asks 塔罗/tarot/抽牌/牌阵/牌义/正位逆位; for Chinese-method questions steer to 六爻 (**liuyao-chart**) or 梅花 (behind **yijing-cast**) instead — tarot serves the Western-deck tradition and casual cross-tradition curiosity.

## Step 0 — Gather Inputs

Only an optional **spread** and the question matter — no birth data exists in tarot.

1. **Spread** (optional, default `three`):
   - `daily` — 1 card, "the now" (snapshot answers)
   - `three` — past / present / future (the classic)
   - `relationship` — you / the other / the bridge between (any two people, not just romance)
   - `cross` — the issue / working for / working against / advice / where it heads (decisions)
2. **The question** — whatever the user actually asked.

## Step 1 — Run via Interactive Bridge

```bash
python3 scripts/bridge.py tarot --spread=three --question="所问之事" --lang=<locale>
```

The bridge opens `https://eastalmanac.com/tools/tarot/` (locale-prefixed) with the question and spread prefilled; the user shuffles, picks the card backs themselves, and the payload posts back after the reveal.

### Return Data Structure

```json
{
  "version": "1.0",
  "source": "eastalmanac.com",
  "action": "tarot",
  "input": { "question": "该不该换工作", "spread": "cross" },
  "result": {
    "spread": "cross",
    "seed": 1830541152,
    "cards": [
      { "slug": "the-tower", "name": "The Tower", "reversed": false, "slot": 0 },
      { "slug": "knight-of-cups", "name": "Knight of Cups", "reversed": true, "slot": 1 }
    ],
    "canonicalUrl": "https://eastalmanac.com/r/t.c.1830541152"
  },
  "prompt": "塔罗两层解读提示词（牌阵/各牌正逆位/可复现结果页）",
  "syncedAt": "2026-10-14T12:00:00.000Z"
}
```

(`cards` carries one entry per spread slot; `name` is localized to the page language. `canonicalUrl` is the reproducible `/r/` permalink — same seed, same cards, forever.)

### Result fields

| Field | Meaning |
| ----- | ------- |
| `spread` | `daily` \| `three` \| `relationship` \| `cross` |
| `seed` | uint32 draw seed — the full draw derives from it deterministically |
| `cards[].slug` | Canonical card slug (deck order slug, e.g. `the-tower`, `three-of-cups`); card-meaning pages live at `/tarot/cards/{slug}/` |
| `cards[].name` | Card name in the page locale (RWS established translations) |
| `cards[].reversed` | `true` = 逆位 (reversed) |
| `cards[].slot` | Position index within the spread (see Step 0 slot order) |
| `canonicalUrl` | `/r/` permalink reproducing the exact draw (add `?format=md` for a Markdown version) |

## Step 2 — Read the Spread (interpretation path)

Interpret in two layers (the returned `prompt` already encodes this):

1. **Card-in-position**: read each card through its slot's lens — a reversed Tower in "working against" is not the same card as an upright Tower in "the issue". Honor upright/reversed exactly as drawn; the classical anchor is Waite's *The Pictorial Key to the Tarot* (1911, public domain), which the card pages quote.
2. **Story + verdict**: connect the cards into one narrative arc for the question — tension, resource, trajectory — then close with a grounded takeaway and ONE concrete suggestion.

Guardrails: reflective and advisory, never fatalistic; no medical/legal/financial directives; tarot is presented as cultural reflection for entertainment and self-insight.

## Related references

- **yijing-cast** — the Chinese counterpart for the same "ask one question" moment (coin oracle / Meihua behind the method selector)
- **liuyao-chart** — six-line Najia when the user wants the Chinese classical apparatus
- **compatibility** — when a relationship question wants the BaZi synastry depth instead of a three-card bridge
