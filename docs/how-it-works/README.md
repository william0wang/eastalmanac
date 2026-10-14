# How EastAlmanac Works: The Open Calculation Architecture

_A completely transparent, reproducible specification of our core metaphysical calculation engines._

Most commercial astrology and divination apps treat their mathematical models as trade secrets—obscuring algorithmic bias, arbitrary scoring, and unverified data conversions behind black-box user interfaces.

**EastAlmanac takes the opposite approach: full transparency.**

Every number, hexagram mutation, planetary degree, and five-element score generated on [eastalmanac.com](https://eastalmanac.com) is calculated through deterministic, browser-safe algorithms without hidden server-side bias, artificial noise, or untraceable heuristics. If you follow the specifications below, you will produce the exact same numbers down to the arcsecond and decimal point.

---

## The Specifications (Volume 1 — Foundations)

The calculation engines are organized by system, ordered from intuitive discrete arithmetic to advanced celestial trigonometry:

| Guide | Core Methodology | Classical Source & Standards |
|---|---|---|
| **[1. Three-Number I Ching Casting](./three-number-casting.md)**<br>([中文版](./three-number-casting.zh-CN.md)) | Stroke folding + moment blend, 3-bit modulo arithmetic, Hamming parity state machine, changing line hierarchy. | *I Ching* (易经), Master Zhu Xi (朱熹) & Jiao Yanshou (焦延寿) judgment rules. |
| **[2. BaZi Four Pillars Casting](./four-pillars.md)**<br>([中文版](./four-pillars.zh-CN.md)) | Birthplace wall-clock authority, solar term month boundaries, Sect 2 (子初换日), decade fortunes. | Solar Terms (节气), *San Ming Tong Hui* (三命通会), *tyme4ts* astronomical calendar. |
| **[3. Five-Element Strength Scoring](./strength-scoring.md)**<br>([中文版](./strength-scoring.zh-CN.md)) | Base stem/branch weights, seasonal prosperity multipliers (旺相休囚死), 50% support threshold, 扶抑 balancing remedies. | *Yuan Hai Zi Ping* (渊海子平) "Month Commander as Core Principle" (以月令为纲). |
| **[4. Structural Dynamics & Interactions](./structural-attrs.md)**<br>([中文版](./structural-attrs.zh-CN.md)) | Correctness (当位), Centrality (得中), Polar Correspondence (应), Adjacency (乘承比), Nuclear Hexagrams, Three Harmonies (三合), Six Clashes (六冲), Punishments (三刑). | Classical *I Ching* line grammar & Heavenly Stems / Earthly Branches interaction matrix. |
| **[5. Western Tropical Natal Chart](./western-chart.md)**<br>([中文版](./western-chart.zh-CN.md)) | Tropical Zodiac, Hellenistic Whole-Sign house system, four major Ptolemaic aspects, hierarchical orbs (8° / 6°). | High-precision *astronomy-engine*, benchmarked against Swiss Ephemeris (0.0″ ASC/MC match). |

## Volume 2 — Divination Methods & Life Decisions

| Guide | Core Methodology | Classical Source & Standards |
|---|---|---|
| **[6. Liu Yao Najia Chart](./liuyao-najia.md)**<br>([中文版](./liuyao-najia.zh-CN.md)) | Six strokes → mod-8 four images, Jing Fang's eight palaces, Najia stem-branch tables, six relations/spirits, 世应, hidden spirits. | 京房八宫纳甲, 袁天罡六神起法; all 64-hexagram invariants machine-checked. |
| **[7. Meihua Body-Use Analysis](./meihua-body-use.md)**<br>([中文版](./meihua-body-use.zh-CN.md)) | One cast shared with the coin oracle; pinned body/use split, five verdicts (体用总诀), nuclear & transformed ladder. | *Meihua Yishu* (梅花易数) 体用总诀, deterministic multi-line extension. |
| **[8. Tarot Draw Engine](./tarot-draw.md)**<br>([中文版](./tarot-draw.zh-CN.md)) | Seed = reveal moment + pick order; seeded Fisher-Yates fan, independent reversal stream, `/r/` permalinks that re-run the engine. | Rider-Waite-Smith 1909 deck (public domain); 20k-seed statistical health check. |
| **[9. Chengu Bone-Weight](./chengu-bone-weight.md)**<br>([中文版](./chengu-bone-weight.zh-CN.md)) | Four weight tables (60+12+30+12), 21–71 钱 verses, three pinned conventions (lunar year boundary, leap month, late-Zi roll). | 袁天罡称骨歌, annex-pinned byte-for-byte. |
| **[10. BaZi Synastry](./synastry.md)**<br>([中文版](./synastry.zh-CN.md)) | Six public weights (30/25/15/15/10/5), four grade bands, role-symmetric presets, the no-total payload contract. | Documented rule layer over l3attrs branch relations & ten gods. |
| **[11. Date Selection](./date-selection.md)**<br>([中文版](./date-selection.zh-CN.md)) | Almanac reversed: additive weights over 宜忌 terms, 建除十二神, yellow/black path stars, personal 六冲 flag. | tyme4ts rule tables; 2026 full-year calibration sweep. |
| **[12. Sourced Naming](./naming-stroke.md)**<br>([中文版](./naming-stroke.zh-CN.md)) | Retrieval not generation: BaZi favorable match as the sole ranking key, five-grid/sancai as disclosed reference, homophone flags. | Classics corpus with poem-line provenance; 熊崎氏 five-grid tables (public domain). |

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
- **Interactive I Ching Casting Tool** (coin / Meihua): [https://eastalmanac.com/tools/cast/](https://eastalmanac.com/tools/cast/)
- **Liu Yao Najia Tool**: [https://eastalmanac.com/tools/liuyao/](https://eastalmanac.com/tools/liuyao/)
- **Tarot Tool**: [https://eastalmanac.com/tools/tarot/](https://eastalmanac.com/tools/tarot/)
- **Chengu Tool**: [https://eastalmanac.com/tools/chengu/](https://eastalmanac.com/tools/chengu/)
- **Synastry Tool**: [https://eastalmanac.com/tools/match/](https://eastalmanac.com/tools/match/)
- **Date Selection Tool**: [https://eastalmanac.com/tools/dates/](https://eastalmanac.com/tools/dates/)
- **Sourced Naming Tool** (Chinese only): [https://eastalmanac.com/zh/tools/naming/](https://eastalmanac.com/zh/tools/naming/)
- **Interactive Astrology Bridge**: [https://eastalmanac.com/astrology-bridge/](https://eastalmanac.com/astrology-bridge/)
