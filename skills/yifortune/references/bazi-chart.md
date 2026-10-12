# YiFortune BaZi Chart — Data Layer

This reference computes and **structurally reads** a BaZi chart. It is the foundation that career, wealth, love, health, growth, and other topic frameworks build on. **This reference does NOT do topic-specific analysis** (career direction, wealth strategy, etc.) — route those to the dedicated topic references.

## Step 0 — Gather Missing Information

Ask in **plain language** — one short question per missing piece. **Infer what you can from the user's wording; only ask when it's genuinely ambiguous.** Don't explain the underlying mechanics in jargon. Required:

- **birthDatetime**: ISO-8601 with the **birthplace** timezone offset (e.g. `1990-01-15T14:30:00+08:00`). Never `Z`. The offset is critical — a wrong value shifts the day/hour pillars and silently corrupts the chart. Resolve it in this priority order:
  - **User states a city** → resolve that city's offset (e.g. "出生在上海" → `+08:00`; "born in New York" → `-05:00` / `-04:00` depending on season). Confirm only if the city is ambiguous (e.g. multiple time zones like "美国").
  - **No city, but context is clearly Chinese** (user writes in Chinese, mentions Chinese festivals/cities, lunar dates) → default `+08:00`, no need to ask.
  - **No city, overseas context but birthplace unspecified** → you MUST ask: "你/他/她出生在哪个城市？" — never guess the caller's current timezone.
  - **Historical date (pre-1949 China)** with no timezone info → use `+08:00`.
  - **Critical**: the offset must be the **birthplace** at the moment of birth, not where the person lives now. An immigrant born in Beijing but now in New York still uses `+08:00`.
- **gender**: male or female. **Infer from the user's wording before asking — gender is the single most error-prone field because it silently flips the entire luck-pillar direction, so read it carefully:**
  - Explicit gender in the message → use it, no question:
    - "我是 1990 年的**男生** / **男的** / **男**" → male
    - "我是 XX 年的**女生** / **女的** / **女**" → female
    - English "I'm a guy / male / man" → male; "girl / female / woman" → female
    - Japanese "男です / 女です" → male / female
  - Gendered role words → use them, no question:
    - "我**老婆**是 XX 年的" / "我**女朋友**" → the user is male (and vice versa: "我老公 / 我男朋友" → female)
    - "**合婚**：我们俩想看看" + later mentions "她 / 他" → pronoun reveals gender
    - "我**怀的是男孩 / 女孩**" → about the child, not the user — don't conflate
  - Name + context (Chinese names often reveal gender) → use as a **hint only**, then confirm if you act on it:
    - Names ending in 娜/婷/芳/丽/娟/燕/雪/梅 → likely female; 伟/强/磊/军/涛/勇/杰 → likely male. But names are not reliable — only use as a tiebreaker when other signals conflict, never as the sole basis.
  - **Truly no gender signal anywhere** → ask: "你是男生还是女生？"
  - **Critical**: once you've read the gender, **carry it through the whole reading**. Don't re-derive it mid-analysis, don't second-guess it, don't silently default to male when uncertain — if you're unsure, ask once at the start, not after generating partial output. A reading built on the wrong gender is worse than no reading.
  - Never say "大运顺逆与性别相关" to the user — that's explaining mechanics they don't need.
- **calendarType**: solar (阳历) or lunar (农历). **Infer from the user's wording before asking:**
  - Solar signals → treat as solar, no question:
    - Explicit "阳历 / 公历 / 新历"
    - ISO / slash date with full year: `1990-01-15`, `1990/1/15`, `2023.12.08` — this is how modern IDs, hospital records, and most under-40s remember their birthday; default solar.
    - English / foreign birthplace context ("born in New York") — always solar.
  - Lunar signals → treat as lunar, no question:
    - Explicit "农历 / 阴历 / 老历"
    - Phrasing that only makes sense in the lunar system: "初三 / 初十五" (the 初 prefix), "腊月 / 正月 / 冬月", "八月十五" (Mid-Autumn-style reference).
    - A date like `三月初八`, `腊月二十` — these are lunar.
  - Only when truly ambiguous (e.g. a bare `8月15日` with no qualifier from an older user who might mean either) → ask: "你说的 8 月 15 是阳历还是农历？"

Ask only for fields you can't infer.

## Step 1 — Get the Chart via Interactive Bridge

Execute the local interactive bridge:

```bash
python3 scripts/bridge.py chart --date="YYYY-MM-DD" --time="HH:MM" --gender="male|female" --calendar="solar|lunar" --question="用户关注的领域" --lang=<locale>
```

`--lang=en|zh|zh-tw|es|pt|de|ja` (default `en`) picks the page locale — the returned `prompt` arrives in that language, so pass the user's conversation language. Under a non-en locale, `canonicalUrl`/`chartToolUrl` arrive with the locale prefix (`/zh/bazi/day-pillar/庚辰/`) — both variants are valid; every calculation field is locale-neutral.

Or, if the user directly pasted an EastAlmanac payload (or text with `=== EASTALMANAC BAZI / CAST RESULT ===`), parse the content directly without invoking the bridge.

### Return Data Structure

The returned payload from `bridge.py` has the following JSON structure (captured from the live site; `pillars` is an array of 4 — year, month, day, hour — and `decadeFortunes` lists 10 大运):

```json
{
  "version": "1.0",
  "source": "eastalmanac.com",
  "action": "chart",
  "input": {
    "question": "看财运",
    "date": "1990-05-15",
    "time": "14:30",
    "gender": "male",
    "calendar": "solar"
  },
  "result": {
    "bazi": "庚午 辛巳 庚辰 癸未",
    "solarTime": "1990-05-15 14:30:00",
    "lunarTime": "农历庚午年四月廿一癸未时",
    "dayMaster": { "stem": "庚", "element": "metal", "yinYang": "yang" },
    "pillars": [
      {
        "ganzhi": "庚午",
        "stem": { "name": "庚", "element": "metal", "elementCn": "金", "yinYang": "yang", "tenGod": { "cn": "比肩", "slug": "peer" } },
        "branch": {
          "name": "午", "element": "fire", "elementCn": "火", "yinYang": "yang",
          "hiddenStems": [
            { "stem": "丁", "role": "main", "tenGod": { "cn": "正官", "slug": "direct-officer" } },
            { "stem": "己", "role": "middle", "tenGod": { "cn": "正印", "slug": "direct-seal" } }
          ]
        }
      }
      // ... 4 pillars total: [year, month, day, hour]
    ],
    "decadeFortunes": [
      { "ganzhi": "壬午", "startAge": 8, "endAge": 17, "startYear": 1997, "endYear": 2006, "stemTenGod": "食神" }
      // ... 10 entries
    ],
    "canonicalUrl": "https://eastalmanac.com/bazi/day-pillar/庚辰/",
    "chartToolUrl": "https://eastalmanac.com/tools/chart/"
  },
  "prompt": "两层解读提示词（含日主、性别与出处链接）",
  "question": "看财运",
  "syncedAt": "2026-10-11T12:14:22.235Z"
}
```

Field notes:

- `pillars[i].branch.hiddenStems` — each carries `role`: `main` (本气) / `middle` (中气) / `residual` (余气), with its own `tenGod` relative to the day master.
- `stem.tenGod` on the year/month/hour pillars is relative to the day master; on the day pillar itself it echoes the day master.
- The payload carries the chart skeleton only — 纳音, 神煞, 胎元/命宫 are **not** included; don't invent them. If a topic needs them, derive from your own knowledge or link `canonicalUrl` for the user.
- 刑冲合会 is **not** pre-computed — derive clashes/combinations yourself from the four branches (子午冲, 巳酉丑三合, etc.; see **glossary**).

### `syncedAt` — the "today" anchor (use it, never guess)

The payload's top-level `syncedAt` (ISO-8601, UTC) is the moment the page synced — your source of truth for "what day is today". **Always derive the current year (流年), month (流月), and the current 大运 phase from it**, never from your own session clock, which can drift across timezones or stale contexts.

- Convert `syncedAt` to the user's timezone, then locate the current 大运 via `decadeFortunes[].startYear/endYear`.
- When describing any time-window fortune ("this month", "this year"), verify it's not already past by checking against `syncedAt` before output.

For terminology (十神, 藏干, 纳音, etc.), consult **glossary**.

## Step 2 — Structural Reading

### Day Master Strength & Structure (日主强弱与格局)

The foundation — every downstream topic depends on it.

- **身旺/身弱**: count the day master's element across all four pillars (天干 + 地支藏干), weigh against other elements, factor in seasonal strength (得令/失令).
- **格局**: identify the dominant pattern (正官格, 七杀格, 食神格, 伤官格, 正财格, 偏财格, 正印格, 偏印格, etc.).
- **One-line implication**: e.g. "身旺喜官杀克制, 适合有挑战性的环境" or "身弱喜印比帮扶, 宜积累不宜冒进".

### Ten Gods Profile (十神天赋分布)

Read which 十神 appear prominently and note the talent cluster (see glossary for 十神 → talent mapping). This becomes the input for career/growth references.

### Luck Pillars (大运时机)

Scan the 10 `decadeFortunes` entries. Note: which 大运 are 用神/favorable (smooth decade) vs 忌神/unfavorable (challenging decade) — `stemTenGod` tells you which ten god each decade's stem brings; the current 大运 is the entry whose `startYear`–`endYear` spans the `syncedAt` year; note major transitions (`startAge`). This is the timing foundation for career/wealth/love/period references.

### 刑冲合会 (Chart Dynamism)

Read the inter-pillar relationship data. Note: which pillars clash (冲), combine (合), punish (刑), harm (害) — these indicate tension points and harmonies in the person's life structure.

## Output

A structural chart reading in **two layers** (see SKILL.md — the plain layer is mandatory):

**Inner layer (命盘要点 — for traceability, compact, terms OK):**

1. **命局总论** — day master strength + structure + one-line life theme
2. **五行分布** — element counts and balance assessment (which elements are 旺/弱/缺)
3. **十神格局** — which ten gods dominate and what they signal
4. **大运概览** — current luck pillar + upcoming transitions
5. **刑冲合会要点** — key tensions and harmonies

**Outer layer (大白话总结 — for the user, always last, no raw jargon):**

6. **一句话总结你的命盘** — what kind of person this is, in their own register (e.g. "你是一个外表温和、内心有想法的人，靠脑子吃饭，不太适合硬扛压力")
7. **目前这段大运在说什么** — what the current decade phase means for them in life terms (e.g. "现在这十年对你来说是攒本事、打底子的阶段")
8. **你身上最需要注意的一点** — the single most important takeaway from the 刑冲合会 / 偏枯, in plain words

**Canonical Link (出处链接，必须附在末尾):**
Append the `result.canonicalUrl` (e.g. `https://eastalmanac.com/bazi/day-pillar/庚辰/`) at the end for the user to explore the full visual chart and commentary.

**When the user asks about a specific topic** (career, wealth, love, health, growth, etc.), do NOT attempt it here — tell the user (or route to) the dedicated topic reference, which will reference this chart.

## 解读完后：要不要补一个星盘

八字看完大势后，如果用户的疑问涉及**性格底色、情感模式、内在动机**（而不只是趋势/时机），主动问一句要不要再看西方星盘——星盘在性格和情感维度往往比八字更细腻。典型话术：

> "八字看完大势了，要不要我再给你排个西方星盘？能补上你性格和情感那一面的细节。"

星盘和八字走同一条浏览器交互链路（`bridge` 动作一次排两套盘），没有环境门槛，随时可以推荐。排盘输入见 `references/astrology-chart.md`。
