# EastAlmanac Chengu Bone-Weight Reckoning (称骨算命) — Data Layer

**称骨** (attributed to 袁天罡, Tang dynasty) is a folk method: convert a birth date + hour into four weights (年/月/日/时, in 两/钱), sum them, and read the matched 批注诗 (verdict verse). It is a **quick, coarse folk reckoning** — not a substitute for a full BaZi chart. Route here when the user explicitly asks 称骨/称骨算命/骨重/袁天罡称骨; for a serious life-topic reading, BaZi (**bazi-chart**) is the real tool — offer chengu as a light add-on, not the main course.

## Step 0 — Gather Inputs

Birth **date + hour** are both required (four weights: year/month/day/hour). Calendar can be solar or lunar — the page converts. The hour only needs the rough 时辰 (2-hour bin); "早上 5 点多" is enough to pick 卯时.

1. **Birth date** — YYYY-MM-DD (state solar or lunar)
2. **Birth hour** — HH:MM or a rough 时辰
3. (Optional) what they want it read toward (运势/性格/晚年…)

## Step 1 — Run via Interactive Bridge

```bash
python3 scripts/bridge.py chengu --date="YYYY-MM-DD" --time="HH:MM" --calendar="solar|lunar" --question="关注领域" --lang=<locale>
```

The bridge opens `https://eastalmanac.com/tools/chengu/` (locale-prefixed) with the inputs prefilled and auto-computed; the user verifies and clicks **「⚡ 回传给终端 Agent」** to post the payload back.

### Return Data Structure

```json
{
  "version": "1.0",
  "source": "eastalmanac.com",
  "action": "chengu",
  "input": { "question": "", "date": "1971-01-27", "time": "00:30", "calendar": "solar" },
  "result": {
    "yearGanzhi": "辛亥",
    "lunarMonth": "正月",
    "lunarDay": "初一",
    "hourBranch": "子",
    "weights": [17, 6, 5, 16],
    "totalLabel": "四两四钱",
    "verse": "来事由天莫苦求，须知福禄胜前途。当年财帛难如意，晚景欣然便不忧。",
    "canonicalUrl": "https://eastalmanac.com/tools/chengu/"
  },
  "prompt": "称骨两层解读提示词（四柱重量/总重/批注诗与出处）",
  "syncedAt": "2026-10-13T12:00:00.000Z"
}
```

(The example is the folk tables' own worked case: 1971-01-27 00:30 solar = 辛亥年正月初一子时.)

### Result fields

| Field | Meaning |
| ----- | ------- |
| `yearGanzhi` | Lunar-year ganzhi (boundary = 正月初一, NOT 立春 — the folk tables' own convention) |
| `lunarMonth` / `lunarDay` | The lunar month/day labels used for the month/day weights (leap month takes the base month's weight) |
| `hourBranch` | The 时辰 branch for the hour weight (23:00 晚子时 counts as the NEXT day) |
| `weights` | [year, month, day, hour] in 钱 (1 两 = 10 钱) — 17 = 一两七钱 |
| `totalLabel` | The summed weight, formatted (range across all births: 二两一 … 七两一) |
| `verse` | The matched 批注诗 — **the primary answer** |
| `canonicalUrl` | The tool page. No per-cast permalink: birth data never enters a URL (privacy) |

These four rules — lunar-year boundary, leap-month base weight, 晚子时 roll, the 钱 arithmetic — are the ones the engine pins; they match the public folk tables, whose own worked examples they were validated against.

## Step 2 — Read the Verse

The verse IS the reading — paraphrase it, don't invent around it:

1. **Inner layer**: the four weights + total, and the verse's beats (this example: 早岁莫强求 → 福禄在后 → 晚景无忧)
2. **Outer layer**: plain-language summary answering what the user asked — what the verse says comes easy vs. late, plus one concrete attitude suggestion. Weight context in one clause at most ("四两四在中段，不算重也不薄"), never a verdict of its own.

Keep it light: 称骨 is a folk parlor reckoning. If the user starts making life decisions off it, gently note it's the coarsest of the site's tools and a full BaZi chart (**bazi-chart**) says far more.

## Output

Two layers (SKILL.md contract). **Canonical Link (附在末尾):** append `result.canonicalUrl` (the chengu tool page).

## Related

- Serious life-arc reading → **bazi-chart** (`bridge.py chart`)
- Today/this-period state → **period-fortune**
