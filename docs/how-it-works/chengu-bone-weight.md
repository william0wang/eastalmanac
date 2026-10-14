# Chengu Bone-Weight Reckoning: Four Tables, Fifty-One Verses, Three Pinned Conventions

_Last verified: 2026-10_

## TL;DR
称骨算命 (bone-weight fortune, attributed to the Tang astronomer 袁天罡) is folk arithmetic: convert a birth date + hour into **four weights** (lunar year / month / day / hour, counted in 钱 qian, 1 两 = 10 钱), sum them, and read the matched 批注诗 (verdict verse). EastAlmanac implements it as a pure table-driven engine: four public-domain weight tables (60 + 12 + 30 + 12 entries) plus a verse for **every** total from 21 to 71 钱. The tables are pinned **byte-for-byte** against an archived source copy, and the three ambiguous conventions most sites leave vague — the lunar-year boundary, leap months, and the late-Zi hour — are pinned and published.

---

## 1. The Four Weight Tables (钱)

**Year weight, by the 60 ganzhi cycle** (甲子 12, 乙丑 9, 丙寅 6, 丁卯 7, … 癸亥 6 — full cycle, indexed by ganzhi number 甲子=0 … 癸亥=59):

```text
12 9 6 7 12 5 9 8 7 8 15 9 16 8 8 19 12 6 8 7 5 15 6 16 15 7 9 12 10
7 15 6 5 14 14 9 7 7 9 12 8 7 13 5 14 5 9 17 5 7 12 8 8 6 19 6 8 16
10 6
```

**Month weight, by lunar month** (正月 6 … 腊月 5):

| 正 | 二 | 三 | 四 | 五 | 六 | 七 | 八 | 九 | 十 | 冬 | 腊 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 6 | 7 | 18 | 9 | 5 | 16 | 9 | 15 | 18 | 8 | 9 | 5 |

**Day weight, by lunar day** (初一 5, 初二 10, 初三 8, 初四 15, 初五 16, 初六 15, 初七 8, 初八 16, 初九 8, 初十 16, 十一 9, 十二 17, 十三 8, 十四 17, 十五 10, 十六 8, 十七 9, 十八 18, 十九 5, 二十 10, 廿一 10, 廿二 9, 廿三 8, 廿四 9, 廿五 15, 廿六 18, 廿七 7, 廿八 8, 廿九 16, 三十 6)

**Hour weight, by the hour branch** (子 16, 丑 6, 寅 7, 卯 10, 辰 9, 巳 16, 午 10, 未 8, 申 8, 酉 9, 戌 6, 亥 6)

The four weights sum to **21–71 钱**; every total in that range has a verse (machine-verified — see §5).

## 2. The Three Pinned Conventions

The folk tables are silent on edge cases most implementations hand-wave. EastAlmanac pins and publishes all three:

1. **Year weight keys on the LUNAR year ganzhi, switching at 正月初一** (lunar new year) — the convention the folk tables' own worked examples use. This *deliberately differs* from the site's BaZi engine, whose year pillar switches at 立春. Chengu is a lunar-calendar folk method; BaZi is a solar-term system — each keeps its native boundary.
2. **A leap lunar month takes the weight of the month it leaps** (整月归月 — no first-half/second-half split). 闰六月 weighs as 六月.
3. **晚子时 (23:00–24:00) reckons as the NEXT lunar day** — the folk "夜11–12点算次日" rule. The calendar library keeps the clock day, so the engine rolls it explicitly; year, month, and day weights all follow the rolled day.

## 3. The Verdict Verses

One verse per total, 51 in all (二两一钱 through 七两一钱), stored as the public-domain classical text. Sample — 四两四钱 (4 liang 4 qian):

> 来事由天莫苦求，须知福禄胜前途。当年财帛难如意，晚景欣然便不忧。

The full set lives in the engine (and its archived source copy — see §5); totals format as 「X两Y钱」 (zero qian → 「X两」).

## 4. Worked Golden Examples

**The source's own example — 1971 正月初一 子时:**

| Component | Key | Weight |
|---|---|---|
| Year | 辛亥 | 17 |
| Month | 正月 | 6 |
| Day | 初一 | 5 |
| Hour | 子 | 16 |
| **Total** | | **44 钱 = 四两四钱** |

→ the verse above.

**甲子年正月初一子时** → 12 + 6 + 5 + 16 = **39 钱（三两九钱）**.

**Solar input 2026-10-13 14:30** (the page converts solar→lunar) → 丙午年 九月 初四 未时 → the four weights of those keys.

**Edge conventions in action:** `2026-10-13 00:30` (early Zi) reckons as 初四; `2026-10-13 23:30` (late Zi) rolls to **初五**; `2025-07-29` lands in 闰六月 and takes the **六月** weight.

## 5. Engine Invariants (machine-checked)

- Every total 21–71 钱 is **reachable** by some year×month×day×hour combination, and every total has a verse.
- The four tables and all 51 verses match the archived annex copy (`chengu-ben.json`) **byte-for-byte**, with its provenance record.
- Folk editions genuinely diverge row-by-row; the engine pins the one archived 底本. Two known cross-edition splits, both kept as the 底本 reads: the 二十 day weight (10 钱 here; one widely-circulated edition lists 15 钱) and the 三两六钱/三两九钱 verse pair (男命/女命 annotated editions swap the two verses; the 底本 and the simplified 通行本 agree with the engine's placement).
- The 60-entry year table round-trips: every valid ganzhi resolves, invalid pairs (e.g. 甲丑 — stem/branch parity mismatch) are rejected.

## 6. Positioning — an Honest Boundary

Chengu is a **quick, coarse folk reckoning**: four integers and a lookup. It cannot see the interactions a full BaZi chart reads (ten gods, palaces, luck pillars). The site offers it as exactly that — a light folk snapshot, never a substitute for the full chart.

---

## Try It Online
- **Chengu Tool**: [https://eastalmanac.com/tools/chengu/](https://eastalmanac.com/tools/chengu/)
