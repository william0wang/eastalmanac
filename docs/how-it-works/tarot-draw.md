# The Tarot Draw Engine: Seeded Shuffles, Reversal Streams, and Permalinks That Cannot Drift

_Last verified: 2026-10_

## TL;DR
Tarot on EastAlmanac uses the classic **Rider-Waite-Smith (RWS 1909)** deck — all 78 cards — and a draw engine with the same purity contract as the I Ching engine: **no `Math.random()`, no clock inside**. The page folds the reveal moment plus the order in which the user picked the card backs into a single 32-bit **seed**; a seeded Fisher-Yates shuffle then fans the deck, and an independent hash stream decides each slot's upright/reversed orientation. Same seed → the same draw forever. The `/r/` permalink carries `{spread, seed}` and the edge renderer simply re-runs the engine — **a share link can never drift from what the user actually drew**.

---

## 1. The Deck

78 cards in fixed deck order: the 22 Major Arcana (`the-fool` … `the-world`, deck indices 0–21), then the four suits — Wands, Cups, Swords, Pentacles — each Ace through King (indices 22–77). The engine's `TAROT_DECK` slug list and the card data file (`cards.json`) are asserted identical by the test suite: one truth, two mirrors, checked against each other so they cannot drift apart.

## 2. The Four Spreads

| Spread | Slots | Positions |
|---|---|---|
| `daily` | 1 | the now |
| `three` | 3 | past / present / future |
| `relationship` | 3 | you / the other / the bridge between |
| `cross` | 5 | the issue / working for / working against / advice / where it heads |

## 3. The Seed: Moment + Pick Order

```text
seed = tarotSeed(momentMs, picks)
     = WangFinalizer( FNV-mix( … FNV-mix( 0x9e3779b9, floor(momentMs) ), picks[0] … picks[n-1] ) )
```

The reveal moment and the pick order are folded into one uint32. **Order matters** — picking backs `[3, 17, 42]` gives seed `1830541152`; picking the same backs as `[42, 17, 3]` gives `1873606150`. The user's choice sequence is part of the 机锋, exactly as the stroke is for the coin oracle.

## 4. The Draw: Seeded Fisher-Yates + an Independent Reversal Stream

**Fan (the shuffled deck):** starting from a hash of the seed, iterate `i` from 77 down to 1; at each step refresh the hash (`WangFinalizer(mix(hash, i))`) and swap position `i` with position `hash mod (i+1)`. Slot *s* of the spread takes card `fan[s]`.

**Orientation:** each slot's upright/reversed bit comes from a *separate* stream — the lowest bit of `WangFinalizer(mix(seed XOR 0x5f, slot))` — so reversal is decided per-slot, not baked into the fan.

Note the fanned deck the user sees on screen is presentation only: the **seed fully determines the draw**; the fan is re-derived, not trusted.

## 5. Worked Golden Examples

| Seed | Spread | Cards (slot order, orientation) |
|---|---|---|
| `0` | daily | Wheel of Fortune — **reversed** |
| `123456789` | three | Death (rev) · Queen of Wands (rev) · Wheel of Fortune (rev) |
| `4294967295` | cross | Queen of Wands (rev) · Death (upright) · Six of Swords (rev) · The High Priestess (rev) · The Moon (upright) |
| `777` | relationship | King of Wands (upright) · Knight of Cups (rev) · Strength (rev) |

These are pinned in the test suite — a mismatch means the draw formula drifted and every shared link in the wild would change meaning.

## 6. Permalinks

Each draw is shareable as `/r/t.<spreadCode>.<seed>` (e.g. `https://eastalmanac.com/r/t.3.123456789`). The spread codes are single letters (`1` daily, `3` three, `r` relationship, `c` cross). Opening the link parses `{spread, seed}` and **re-runs the engine** — the rendered page is the draw itself, not a stored copy.

## 7. Statistical Health (machine-checked)

Across 20,000 seeds: all 78 cards appear in the first slot (each roughly 100–600 times — no card dominates); the reversal rate stays between 47% and 53%. The seeded shuffle behaves like a fair shuffle.

---

## Try It Online
Shuffle and pick the card backs yourself; the seed is taken at your reveal moment:
- **Tarot Tool**: [https://eastalmanac.com/tools/tarot/](https://eastalmanac.com/tools/tarot/)
