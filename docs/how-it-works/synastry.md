# BaZi Synastry: Six Public Weights, Four Grades, and a Deliberately Absent Total

_Last verified: 2026-10_

## TL;DR
Synastry (八字合参) reads **two full BaZi charts against each other** across six weighted dimensions. The methodology is fully public — dimension weights 30 / 25 / 15 / 15 / 10 / 5 — while the payload **never carries a numeric total**: the weighted sum exists only internally to pick a coarse four-tier grade (上吉 / 吉 / 中 / 需经营), because a band avoids false precision in relationship readings. The engine is role-symmetric (Partner A/B — no gendered or fatalistic wording anywhere), and the five relationship presets change the reading *emphasis*, never a score.

---

## 1. The Six Dimensions (public weights, summing to 100)

| Dimension | Key | Weight |
|---|---|---|
| 五行喜用互补 | `element-balance` | 30 |
| 日柱合冲刑害 | `day-pillar` | 25 |
| 生肖关系 | `zodiac` | 15 |
| 十神互动 | `ten-god` | 15 |
| 大运同步 | `luck-sync` | 10 |
| 年柱纳音 | `year-nayin` | 5 |

Grade bands on the internal total: **≥ 75 上吉 · ≥ 55 吉 · ≥ 35 中 · < 35 需经营**.

## 2. How Each Dimension Scores

**五行喜用互补 (30) — mutual, two symmetric directions of 15.** For each element on one side's favorable list (from the strength engine, 用神 first), take its share within the *other* chart, average over the list, and scale linearly: `15 × min(averageShare / 0.30, 1)`. A partner whose chart is rich in what the other needs scores high; both directions must carry. Shares below 0.08 count as "thin", zero as "absent" (both reported as reasons).

**日柱合冲刑害 (25) — additive on a neutral baseline of 12.5.**

| Signal | Delta |
|---|---|
| 天干五合 (stems differ by 5 indices: 甲己 乙庚 丙辛 丁壬 戊癸) | +6 |
| Branch 六合 | +7 |
| Branch 三合 | +4 |
| Branch 六害 | −4 |
| Branch 三刑 | −5 |
| Branch 六冲 | −8 |

巳申 carries both 六合 and 三刑 (合中带刑) — its net +2 is deliberately milder than a clean clash. Identical day pillars are flagged but score neutral.

**生肖关系 (15) — baseline 7, then** 六合 +8 · 三合 +5 · 六害 −4 · 三刑 −4 · 六冲 −7.

**十神互动 (15) — six unordered day-master pairs, no fallback.** Two day masters interact in exactly one of six role-symmetric patterns (fully determined by element relation × polarity match):

| Pair (sorted slugs) | Verdict | Score |
|---|---|---|
| direct-officer + direct-wealth | complementary-structure | 13 |
| eating-god + indirect-seal | expressive-nourishing | 11 |
| peer + peer | steady-peers | 11 |
| direct-seal + hurting-officer | expressive-demanding | 10 |
| indirect-wealth + seven-killings | pressure-dynamic | 5 |
| rob-wealth + rob-wealth | resource-rivalry | 5 |

**大运同步 (10).** Nine samples at ages 20–60 (every 5 years); at each sampled age the two active decade stems are *in step* if same element or either generates the other, *out of step* if one controls the other. Score = 10 × (in-step / compared).

**年柱纳音 (5).** The nayin element is derived from the name's trailing character (all 30 classical nayin names end with their element — 海中金, 大林木…): same element 5 · either generates 4 · controls 1.5.

## 3. The No-Total Contract

The six scores sum to an internal total that picks the grade band — then the total is **stripped before the payload leaves the module**. The UI and the deep-read prompt see the grade plus per-dimension detail with machine-readable reasons (`day-pillar:stem-wu-he`, `zodiac:branch-san-he`, `luck:in-step`, …), never a number like "71.4/100".

## 4. Role Symmetry and the Five Presets

Partners are A/B throughout; classical gendered criteria (one side's "spouse star", spouse-harming verdicts) are generalized into role-symmetric tension points, and fatalistic wording is banned from every string. The relationship presets — 恋爱婚姻 / 上司下属 / 事业伙伴 / 朋友知己 / 家人亲子 — pick which dimensions *lead the reading* (e.g. boss–subordinate leads with ten-god interaction); **every score and grade is identical across presets** — copy adapts, math does not.

## 5. Worked Golden Example

Partner A: 1990-01-15 14:30 male → 己巳 丁丑 庚辰 癸未 (day master 庚 metal, strong; favorable fire, water, wood).
Partner B: 1985-06-15 10:00 female → 乙丑 壬午 乙酉 辛巳 (day master 乙 wood, weak; favorable water, wood).

| Dimension | What fired | Score |
|---|---|---|
| element-balance | mutual favorable coverage 0.22 (A) / 0.066 (B) | 14.3 |
| day-pillar | 庚乙 stem 五合 (+6) and 辰酉 六合 (+7) on the 12.5 baseline | **25 (max)** |
| zodiac | 巳丑 in the 巳酉丑 三合 | 12 |
| ten-god | 庚 views 乙 as direct-wealth; 乙 views 庚 as direct-officer | 13 |
| luck-sync | decades in step at 5 of 9 sampled ages | 5.6 |
| year-nayin | 大林木 (wood) vs 海中金 (metal) — metal controls wood | 1.5 |
| **internal total** | | **71.4 → 吉 (favorable)** |

## 6. Machine-Checked Invariants

- **Symmetric**: swapping A and B leaves every dimension score and the grade unchanged (reason sides mirror).
- **Deterministic** across calls; every dimension score lies in [0, weight] with at least one structured reason.
- The golden pair above is hand-derived from the strength-engine fixtures and pinned in tests; banned strings (克妻 / 克夫 / 离婚) never appear in any preset's output.

---

## Try It Online
- **Synastry Tool**: [https://eastalmanac.com/tools/match/](https://eastalmanac.com/tools/match/)
