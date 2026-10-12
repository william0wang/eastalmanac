# How EastAlmanac Works: The Open Calculation Architecture

_A completely transparent, reproducible specification of our core metaphysical calculation engines._

Most commercial astrology and divination apps treat their mathematical models as trade secrets—obscuring algorithmic bias, arbitrary scoring, and unverified data conversions behind black-box user interfaces.

**EastAlmanac takes the opposite approach: full transparency.**

Every number, hexagram mutation, planetary degree, and five-element score generated on [eastalmanac.com](https://eastalmanac.com) is calculated through deterministic, browser-safe algorithms without hidden server-side bias, artificial noise, or untraceable heuristics. If you follow the specifications below, you will produce the exact same numbers down to the arcsecond and decimal point.

---

## The Specifications (Volume 1)

The calculation engines are organized by system, ordered from intuitive discrete arithmetic to advanced celestial trigonometry:

| Guide | Core Methodology | Classical Source & Standards |
|---|---|---|
| **[1. Three-Number I Ching Casting](./three-number-casting.md)**<br>([中文版](./three-number-casting.zh-CN.md)) | 3-bit modulo arithmetic, Hamming parity state machine, changing line hierarchy. | *I Ching* (易经), Master Zhu Xi (朱熹) & Jiao Yanshou (焦延寿) judgment rules. |
| **[2. BaZi Four Pillars Casting](./four-pillars.md)**<br>([中文版](./four-pillars.zh-CN.md)) | Birthplace wall-clock authority, solar term month boundaries, Sect 2 (子初换日), decade fortunes. | Solar Terms (节气), *San Ming Tong Hui* (三命通会), *tyme4ts* astronomical calendar. |
| **[3. Five-Element Strength Scoring](./strength-scoring.md)**<br>([中文版](./strength-scoring.zh-CN.md)) | Base stem/branch weights, seasonal prosperity multipliers (旺相休囚死), 50% support threshold, 扶抑 balancing remedies. | *Yuan Hai Zi Ping* (渊海子平) "Month Commander as Core Principle" (以月令为纲). |
| **[4. Structural Dynamics & Interactions](./structural-attrs.md)**<br>([中文版](./structural-attrs.zh-CN.md)) | Correctness (当位), Centrality (得中), Polar Correspondence (应), Adjacency (乘承比), Nuclear Hexagrams, Three Harmonies (三合), Six Clashes (六冲), Punishments (三刑). | Classical *I Ching* line grammar & Heavenly Stems / Earthly Branches interaction matrix. |
| **[5. Western Tropical Natal Chart](./western-chart.md)**<br>([中文版](./western-chart.zh-CN.md)) | Tropical Zodiac, Hellenistic Whole-Sign house system, four major Ptolemaic aspects, hierarchical orbs (8° / 6°). | High-precision *astronomy-engine*, benchmarked against Swiss Ephemeris (0.0″ ASC/MC match). |

---

## Architectural Guarantees

1. **Zero Fake Randomness**: Divination engines never invent numbers via `Math.random()`. The intent originates entirely with the seeker.
2. **Local Wall-Clock Authority**: Eastern solar terms and planetary positions correspond to physical celestial coordinates at the place of birth; we reject misleading UTC conversions.
3. **Pure Browser Computation**: The calculation packages execute entirely client-side. Zero personal birth data ever travels to our backend servers.
4. **Reproducible Golden Fixtures**: Every guide includes full worked examples cross-checked against our continuous integration test suites.

---

## Try the Live Engines

Test any chart or cast your hexagram on the live deployment:
- **Interactive BaZi Chart Tool**: [https://eastalmanac.com/tools/chart/](https://eastalmanac.com/tools/chart/)
- **Interactive I Ching Casting Tool**: [https://eastalmanac.com/tools/cast/](https://eastalmanac.com/tools/cast/)
- **Interactive Astrology Bridge**: [https://eastalmanac.com/astrology-bridge/](https://eastalmanac.com/astrology-bridge/)
