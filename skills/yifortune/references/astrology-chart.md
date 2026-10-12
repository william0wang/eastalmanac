# YiFortune Astrology Chart — Data Layer

This reference obtains a western natal chart via the EastAlmanac **astrology-bridge** page — the chart is computed **entirely client-side in the browser** (astronomy engine), side by side with the BaZi four pillars of the same birth moment — then **structurally reads** the result. It is the foundation that love, compatibility, and career frameworks build on. **This reference does NOT do topic-specific analysis** — route those to dedicated topic references.

## Step 0 — Gather Missing Information

Ask in **plain language**. Astrology is extremely sensitive to time and place, but the user doesn't need a lecture on house cusps — just ask for the facts. Required:

- **date** (`YYYY-MM-DD`) and **time** (`HH:MM`) of birth. Astrology is far more time-sensitive than BaZi — the Ascendant moves ~1° every 4 minutes, so a wrong clock hour silently rotates the entire house system. If birth-time uncertainty >15 min, gently flag it: "出生时间记得不太准的话，会稍微影响上升星座的判断，没事，我们先用这个看" — don't paralyze the user with caveat stacks.
- **Birthplace** → resolves to `lat`, `lon`, and `tz` (the UTC **offset in hours at the moment of birth**, e.g. `8`, `-5`, `5.5`). Ask "你是在哪个城市出生的？" and resolve the coordinates yourself. Note DST: "born in New York in July" → `-4` (EDT), not `-5`.
  - If the birth city is one of the site's presets — beijing, shanghai, guangzhou, hongkong, taipei, singapore, tokyo, seoul, sydney, dubai, moscow, london, paris, berlin, newyork, losangeles, vancouver, saopaulo — pass `--city=<key>` and the page fills lat/lon/tz itself (still pass `--tz` when the birth season had DST — presets use standard time).
- **gender**: needed for the BaZi half of the page.
- **Critical**: `tz` is the **birthplace's** offset at the moment of birth, not where the person lives now, and not the caller's current timezone. An immigrant born in Beijing but now in New York still uses `+8`.

## Step 1 — Get the Chart via Interactive Bridge

```bash
python3 scripts/bridge.py bridge --date="YYYY-MM-DD" --time="HH:MM" --gender="male|female" --lat=39.9042 --lon=116.4074 --tz=8 --question="用户关注的领域" --lang=<locale>
```

`--lang=en|zh|zh-tw|es|pt|de|ja` (default `en`) picks the page locale — the returned `prompt` arrives in that language, so pass the user's conversation language. `canonicalUrl`/`chartToolUrl` arrive locale-prefixed; the `western` body/sign slugs stay English under every locale (localize them in your output), and all BaZi fields are unchanged.

The page auto-computes when `date + time + lat + lon` arrive via the URL (always pass `--tz` too — it defaults to +8 and a wrong offset corrupts the Ascendant). The user verifies the birth data on the page, then clicks **「⚡ 回传给终端 Agent」** to return the payload.

**Direct Input / Clipboard Recognition**: if the user pasted an EastAlmanac result (text containing `=== EASTALMANAC ... RESULT ===` or the exported JSON), parse it directly without launching the browser.

### Return Data Structure

```json
{
  "version": "1.0",
  "source": "eastalmanac.com",
  "action": "bridge",
  "input": {
    "question": "我的性格底色",
    "date": "1990-01-15",
    "time": "14:30",
    "gender": "male",
    "city": "custom",
    "lat": 39.9042,
    "lon": 116.4074,
    "tz": 8
  },
  "result": {
    "western": {
      "sun": { "degree": "25°06′", "sign": "Capricorn" },
      "moon": { "degree": "…", "sign": "…" },
      "ascendant": { "degree": "…", "sign": "…" },
      "midheaven": { "degree": "…", "sign": "…" },
      "bodies": [
        { "body": "Sun", "sign": "Capricorn", "degree": "25°06′", "house": 12 }
        // Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto — 10 bodies
      ],
      "aspects": [
        { "type": "trine", "a": "Sun", "b": "Moon", "orb": 1.8 }
        // type ∈ conjunction | opposition | square | trine
      ]
    },
    "bazi": {
      "pillars": "己巳 丁丑 庚子 癸未",
      "dayMaster": { "stem": "庚", "element": "metal", "yinYang": "yang" },
      "zodiac": "蛇",
      "ganzhi": ["己巳", "丁丑", "庚子", "癸未"]
    },
    "canonicalUrl": "https://eastalmanac.com/astrology-bridge/",
    "chartToolUrl": "https://eastalmanac.com/tools/chart/"
  },
  "prompt": "East-meets-west astrology reading prompt (angles + BaZi + source link)",
  "question": "我的性格底色",
  "syncedAt": "2026-10-11T12:00:00.000Z"
}
```

Field notes:

- `degree` is a formatted string (`"25°06′"`); compare tight orbs via `aspects[].orb` (degrees, number), not by parsing degrees.
- Body and sign names are **Capitalized slugs** (`"Sun"`, `"Capricorn"`) — render them in the user's language. Ten bodies only — **no North Node, no Chiron, no retrograde flag**; don't invent them.
- Only **four** aspect types are computed: conjunction (0°), square (90°), trine (120°), opposition (180°). A tight orb (< 2°) is strong.
- The payload carries the **BaZi of the same birth moment** (`result.bazi` — a summary, not the full chart payload: pillars string, ganzhi array, day master, and the 生肖 as a Chinese character like `"蛇"`, while `element`/`yinYang` are English slugs) — use it for the cross-system (八字 × 星盘) readings instead of running a second chart.

## Step 2 — Structural Reading

### The Big Three (三巨头)

The personality core — start here.

| Element          | Field                                | Represents                              |
| ---------------- | ------------------------------------ | --------------------------------------- |
| Sun (太阳)       | `western.sun: { sign }` (+ house via `bodies[0]`) | Core identity, vitality, life direction |
| Moon (月亮)      | `western.moon: { sign }` (+ house via `bodies[1]`) | Emotional needs, inner self, security   |
| Ascendant (上升) | `western.ascendant: { sign }`        | Outward persona, first impression       |

### Ten Planets in Signs & Houses

Each planet = a psychological function. **Sign** = style (how), **House** = life area (where). Read all in `western.bodies` (house is a plain number).

| Planet               | Function                                   |
| -------------------- | ------------------------------------------ |
| Mercury (水星)       | Mind, communication, learning              |
| Venus (金星)         | Love, aesthetics, values                   |
| Mars (火星)          | Drive, desire, conflict                    |
| Jupiter (木星)       | Expansion, opportunity, belief             |
| Saturn (土星)        | Limit, responsibility, mastery             |
| Uranus/Neptune/Pluto | Generational: change/dreams/transformation |

Element (fire/earth/air/water) and quality (cardinal/fixed/mutable) aren't in the payload — derive them from the sign yourself when needed.

### Major Aspects (主要相位)

Read the `western.aspects` array. Note tight orbs (`orb` < 2° = strong). The four computed types:

- **conjunction** (合相, 0°): fusion of energies
- **square** (刑相, 90°): tension → growth through friction
- **trine** (三合, 120°): natural flow, talent
- **opposition** (冲相, 180°): polarity, projection, balance needed

Watch for patterns: a **stellium** (3+ planets in one sign/house), a **T-square** (two planets opposing + both squaring a third), or a **grand trine** (three planets 120° apart).

For terminology, consult **glossary**.

## Output

A structural natal chart reading in **two layers** (see SKILL.md — the plain layer is mandatory):

**Inner layer (星盘要点 — for traceability, compact, terms OK):**

1. **三巨头总论** — Sun/Moon/Ascendant interplay and what it means for the personality
2. **行星分布** — key planets in signs/houses (what's prominent, what's challenged)
3. **相位格局** — major aspects and the dynamic they create (e.g. T-square, grand trine, stellium)

**Outer layer (大白话总结 — for the user, always last, no raw jargon):**

4. **一句话说说你这个人** — synthesize the above into a plain portrait of who this person is (e.g. "你是一个特别看重安全感的人，外表很稳，其实心里戏很丰富")
5. **你身上最明显的天赋** — the single strongest planet/aspect, translated into an everyday strength
6. **你最容易卡住的地方** — the single tightest hard aspect or challenged house, translated into a real-life pattern to watch

**Canonical Link (出处链接，必须附在末尾):**
Append the `result.canonicalUrl` at the end for the user to revisit the full visual chart.

**When the user asks about a specific topic** (love, compatibility, career), do NOT attempt it here — route to the dedicated topic reference.
