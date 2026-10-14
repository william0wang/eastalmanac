# Sourced Naming: Retrieval, Not Generation — Two Layers That Never Merge

_Last verified: 2026-10_

## TL;DR
The naming engine (出典起名) never invents a name. Every candidate is an entry of a **classics-sourced corpus** — names mined from 蒙学 primers, 诗文 classics and their likes, each carrying its exact poem provenance (work, section, verse, line index). Scoring is **two layers that never merge into one number**: the BaZi favorable-element match is the *primary* layer and the **only ranking key**; the five-grid 剖象 (五格) + 三才 reading rides along as a *secondary reference layer* under its own 熊崎氏 provenance disclosure. A 56-rule homophone screen flags awkward 姓+名 readings — it marks, never removes: the decision stays with the humans.

---

## 1. The Corpus — Retrieval, Not Generation

Candidates are corpus entries only (no character is ever combined into a new name by the engine). Each entry carries: the name's characters with per-character five-element label, Kangxi stroke count, common-use rarity tier (《通用规范汉字表》 tier 1/2/3 or outside — rarity is a selling point, never a drop reason), pinyin, and the full **origin record** — the work, section, title, line index, character span, and the verse the name was lifted from. An origin lookup re-finds entries whose provenance span sits within 2 characters of a queried position, so every name can be traced back to its poem line. The strokes throughout this guide are Kangxi stroke counts from the character database — canvas stroke folding belongs to the I Ching casting pipeline and is specified in Guide 1.

## 2. Layer 1 (Primary): BaZi Favorable Match — the Only Ranking Key

Each name character's five element is graded against the birth chart's favorable list (from the strength engine, 用神 first):

| Character role | Value |
|---|---|
| 用神 (the remedy, favorable[0]) | 3 |
| 喜神 (other favorable) | 2 |
| Neutral | 1 |
| 忌神 (unfavorable) | 0 |

```text
baziMatchScore = (Σ per-character values) / (3 × character count)    → 0..1
```

Ranking uses this score and **nothing else**. A name whose every character feeds the chart's need scores 1.0; a 忌神-heavy name scores toward 0 and sinks.

## 3. Layer 2 (Secondary): Five Grids + Sancai — Reference Only

The classical 五格剖象法 (five-grid method) computes five stroke-sum numbers from Kangxi stroke counts (the +1 terms are the method's 虚数 placeholder for a missing outside position):

| Grid | Single-char surname | Compound surname |
|---|---|---|
| 天格 tian | surname + 1 | surname₁ + surname₂ |
| 人格 ren | surname + given₁ | surname₂ + given₁ |
| 地格 di | given₁ + 1 (single given) · given₁ + given₂ | same |
| 外格 wai | 2 (single given) · given₂ + 1 (double given) | surname₁ + 1 (single given) · surname₁ + given₂ (double given) |
| 总格 zong | sum of all strokes | sum of all strokes |

**Golden examples (pinned against the published reference):** strokes `([7], [11,12])` → grids 8 / 18 / 23 / 13 / 30; `([15,17], [10])` → 32 / 27 / 11 / 16 / 42; `([4], [10])` → 5 / 14 / 11 / 2 / 14.

Each grid number maps to an element by its **last digit** (1,2 木 · 3,4 火 · 5,6 土 · 7,8 金 · 9,0 水) and is looked up in the **81 数理表** (numbers > 81 reduce by 80: 85 → 5). The 三才 (heaven-human-earth) trio indexes a 125-entry table (5 elements × 25 combos) for its grade and the pairwise relations — 金样: 天人地 = 木木木 → 大吉 with both relations 同; 木木火 → 大吉 with 人生地; 木金水 → 大凶. Both tables' grade distributions are machine-pinned invariants: 81 数理 — 大吉 22 / 大凶 22 / 吉 16 / 半吉 12 / 凶 9; 三才 125 — 大吉 39 / 大凶 33 / 凶 24 / 吉 19 / 半吉 10.

**Provenance, pinned and disclosed**: the 81 and 125 tables are transcribed from the pinned MIT-licensed package shunshi-naming-core@0.1.0 (github.com/shunshi-ai/naming-mcp, MIT © 2026 Shunshi.AI) that reproduces the 熊崎健翁 lineage (d. 1961 — public domain since 2011). Only grade levels and the classical 数理名 poem titles are carried (白话释义 are written fresh); contested numbers (42, 49) are filed 半吉 rather than force-graded. The tool page footer carries a fixed disclosure: 熊崎氏体系（1918）仅供参考.

## 4. The Homophone Screen — Flags, Never Filters

56 curated rules screen the joined 姓+名 reading for awkward homophones — curated families: negation heads (吴→无×, 梅→没×, 夏→下×, 范→犯×/饭×), body/animal readings (朱→猪×, 庞→膀胱, 杨→阳痿), and the classic meme names (史珍香, 杜子腾, 朱逸群). Tone is ignored (连读 teasing ignores tones); an unresolved pinyin simply cannot be screened. **The screen never removes or down-ranks a candidate** — it returns flags; the decision stays with the parents.

## 5. Why Two Layers, Never Blended

Blending a chart-need score with a stroke-numerology score into one number would let a pretty 五格 wash out an unfavorable element — or vice versa. The engine's contract: 喜用 decides the order; 五格/三才 is carried alongside as clearly-labeled classical reference under its own disclosure. The two numbers never touch.

---

## Try It Online
- **Sourced Naming Tool** (Chinese only): [https://eastalmanac.com/zh/tools/naming/](https://eastalmanac.com/zh/tools/naming/)
