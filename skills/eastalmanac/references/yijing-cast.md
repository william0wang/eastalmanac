# EastAlmanac I Ching Divination — Data Layer

This skill casts a hexagram and **structurally reads** the result. I Ching is for **specific questions and decisions** — not general personality readings.

## Core Principle — The Diviner Must Cast

A hexagram is only meaningful when the **user personally** initiates it. NEVER generate, guess, or auto-fill the divination numbers yourself — doing so produces a meaningless hexagram and violates the entire premise of I Ching.

Through the EastAlmanac interactive bridge, the user casts the hexagram themselves on the visual canvas. Your role is to **clarify their specific question**, invoke `bridge.py cast`, and interpret the structured result returned from the user's casting.

## Step 0 — Gather the Question

Plain-language conversation. The I Ching answers a **specific** question, so a vague "帮我算一卦" needs narrowing — but frame it as a real-life question, not a category picker:

> ❌ Don't: "请问您想就什么事起卦? 事业、感情、还是某个具体决定?" (menu-style)
> ✅ Do: "你心里现在最挂念的是哪件事？可以说说看，越具体越好，比如'该不该接受这个 offer'。"

## Step 1 — Cast via Interactive Bridge

Run the interactive bridge:

```bash
python3 scripts/bridge.py cast --question="用户所问之事" --lang=<locale>
```

`--lang=en|zh|zh-tw|es|pt|de|ja` (default `en`) picks the page locale — `benGua.name`/`essence`, `zhiGua.name`, and the returned `prompt` arrive in that language, so pass the user's conversation language. `canonicalUrl` arrives locale-prefixed (`/zh/yijing/22/4`) — use it as-is; `shareUrl` and all numeric fields are locale-neutral.

The bridge opens `https://eastalmanac.com/tools/cast/?q=...` in the user's browser (locale-prefixed when `--lang` is set), where they can interactively draw strokes on the canvas to cast the hexagram. After casting, clicking **「⚡ 回传给终端 Agent」** sends the structured data back to the bridge via the loopback HTTP server.

**Direct Input / Clipboard Recognition**:
If the user has already visited EastAlmanac and pasted the result (e.g. text containing `=== EASTALMANAC BAZI / CAST RESULT ===` or the exported JSON), parse the payload directly without launching the browser.

### Return Data Structure

The returned payload from `bridge.py` has the following structure (captured from the live site):

```json
{
  "version": "1.0",
  "source": "eastalmanac.com",
  "action": "cast",
  "input": {
    "question": "我今年换工作是否合适？",
    "numbers": [28, 55, 67]
  },
  "result": {
    "benGua": { "kingWen": 22, "name": "Grace", "code": "100101", "essence": "Grace and simplicity. Natural authenticity outshines excessive outward ornament." },
    "zhiGua": { "kingWen": 21, "name": "Biting Through", "code": "101001" },
    "changingLines": [3, 4],
    "dongYao": [2, 3],
    "readLine": 4,
    "canonicalUrl": "https://eastalmanac.com/yijing/22/4",
    "shareUrl": "https://eastalmanac.com/r/y.28.55.67"
  },
  "prompt": "两层解读提示词（含本卦/变卦/动爻/当读之爻与出处链接）",
  "question": "我今年换工作是否合适？",
  "syncedAt": "2026-10-11T12:12:52.273Z"
}
```

### Result fields — and which one to read first

The engine has already computed the hexagrams, applied the classical changing-line selection rules, and picked the line to read. Your job is to read the right field:

| Field | What it contains | How to use it |
| ----- | ---------------- | ------------- |
| `benGua.kingWen` | Primary hexagram's King Wen number | **Stable identity key** — use this, not `name`, to look up the canon |
| `benGua.name` / `essence` | Hexagram name + one-line essence (in the `--lang` locale, default `en` — "Grace" in English, "贲" in Chinese) | Title + quick orientation; always render the name in the user's language |
| `zhiGua` | The transformed hexagram (same shape as `benGua`) | Where the situation is heading |
| `changingLines` | Changing-line positions, 1-based (bottom = 1) | How many and which 爻 are moving |
| `dongYao` | The same changing lines as 0-based indexes (bottom = 0) | Redundant with `changingLines`; prefer the 1-based `changingLines` |
| **`readLine`** | **The line the classical rules say to read first** (already selected: 0 = the hexagram judgment 卦辞, 1–6 = that line of 本卦) | **PRIMARY answer anchor** |
| `canonicalUrl` | The exact hexagram/line page on EastAlmanac | The source link to append for the user |
| `shareUrl` | Permalink of this exact cast | Alternative share link |
| `syncedAt` | ISO-8601 UTC timestamp of the cast | The "today" anchor for time-sensitive readings |
| `prompt` | Pre-built two-layer reading instruction | Skeleton for your output; your own analysis leads |

### The reading-priority rule (do not get this wrong)

I Ching answers the **changing line** first — a static hexagram is just the backdrop. The site has already run the classical selection rules (0 moving lines → 卦辞; 1 → that line; 2 → the upper moving line; 3 → 本卦+变卦卦辞; 6 → the 变卦) and put the result in `readLine`:

- **`changingLines` non-empty → read `readLine` as the PRIMARY answer.** Quote that line's 爻辞 and verdict from your own knowledge of the canon (keyed by `benGua.kingWen` + line number) — the payload intentionally carries structure, not the classical text. Paraphrase into plain language; `zhiGua` sketches where it leads.
- **`changingLines` empty → `readLine` is 0: read the hexagram judgment (卦辞) as the whole answer.** The situation is static.

This mirrors how a human diviner reads: 动爻为主，卦辞为辅。`readLine` is the line-specific answer; the hexagram essence is the setting. If you need the full classical commentary, the `canonicalUrl` page carries it — but your reading should stand on your own canon knowledge; don't block on fetching.

## Step 2 — Structural Reading

### Branch on `changingLines` — where the answer lives

```
changingLines = []  →  readLine = 0: the hexagram judgment (卦辞) is the whole answer
changingLines ≠ []  →  readLine points to the decisive line; that 爻辞 is the primary answer
```

**Static (`changingLines` empty):** Read the hexagram judgment — quote the 卦辞 of `benGua.kingWen` from your canon knowledge, plus the traditional commentators' overall take. The situation is stable; the overall text is the verdict.

**Has changing lines:** Read the `readLine` line of 本卦 as the primary answer:
- The 爻辞 (line text) and its 白话文 explanation — key it by `benGua.kingWen` + `readLine`
- The classical commentators' verdicts on that line (邵雍's one-liner, 傅佩荣's 时运/财运/家宅/身体 breakdown) — from your canon knowledge
- The **变卦** (`zhiGua`) it transforms into — where the situation is heading

These line-specific verdicts are exactly what answers "this specific thing — should I do it, and how will it go?" Paraphrase them into plain language for the user. Use the hexagram essence (`benGua.essence`) only to sketch the backdrop.

**Multiple changing lines:** `readLine` is the line the classical rules judged most critical — treat it as the lead; the other moving lines add nuance.

**All six lines change:** the hexagram fully transforms — read toward the `zhiGua` outcome direction.

### Fortune verdicts (贞悔亨厉)

Cross-check the verdict words in the 卦辞/爻辞 you quote (元/亨/利/贞/吉/凶/悔/吝/厉/咎) against the action table (see glossary for the full table):

| Verdict  | Action                                   |
| -------- | ---------------------------------------- |
| 元/亨/吉 | Proceed with confidence                  |
| 利       | Seize the opportunity                    |
| 贞       | Hold steady, don't move rashly           |
| 无咎     | Okay to proceed, mind your duties        |
| 悔/吝    | Reflect, adjust, expect minor difficulty |
| 厉       | High alert — danger, but not hopeless    |
| 凶       | Do not act, lay low                      |

## Meihua 体用 — the sibling reading on the same page

The cast page hosts a second method: **梅花易数 (Meihua)**. It shares the SAME strokes, moment, and numbers — the same hexagram — and differs only in the reading frame: instead of 爻辞, it reads the five-element interaction between the two trigrams (体用生克), per the classical 体用总诀.

Launch identically (`python3 scripts/bridge.py cast --question="..." --lang=<locale>`) — the user picks 梅花易数 in the page's method selector (the coin oracle stays the default). Tell which reading came back by `input.method`: `"meihua"` → read the `tiYong` panel below; `"coin"` → the classical 爻辞 flow above.

### The `tiYong` panel (present only when `input.method === "meihua"`)

```json
"tiYong": {
  "ti": "离火",
  "yong": "坎水",
  "huGua": "既济",
  "ladder": ["用卦坎:生体", "互卦上互·兑:体克", "互卦下互·离:比和", "变卦乾:比和", "变卦坤:生体"]
}
```

| Field | Meaning |
| ----- | ------- |
| `ti` / `yong` | Body (体) and use (用) trigrams as `<trigram><element>` — e.g. "离火" is the Fire trigram Li. **`null` on a fully static cast**: no body/use split exists, and the hexagram judgment (卦辞) stays the whole reading, exactly as the coin method reads it. |
| `huGua` | The nuclear hexagram 互卦 (lines 2–4 as lower, 3–5 as upper, 1-indexed) — the middle passage of the matter. |
| `ladder` | The reading ladder in order: 用卦 → 互卦 (上互, 下互) → 变卦 (upper, lower), each as `frame·label:relation`. |

### How the engine assigns 体 and 用 (pinned, deterministic)

- **用 = the trigram containing the moving lines**; the quiet trigram is 体.
- Both trigrams moving → the one with MORE moving lines is 用; a tie goes to the upper trigram.
- A coin cast can move multiple lines — the classical Meihua time-cast never could — so the engine pins this ONE deterministic assignment instead of leaving it to judgment.

### The five relations (体用总诀)

| `ladder` relation | Verdict | Plain reading |
| ----------------- | ------- | ------------- |
| `生体` (use generates body) | 大吉 | The matter comes to feed you — best case |
| `体克` (body overcomes use) | 小吉 | You control the matter — favorable, effort pays |
| `比和` (same element) | 吉 | Smooth fit, low friction |
| `体生` (body generates use) | 耗泄 | You are spending yourself into the matter — costly |
| `克体` (use overcomes body) | 受制 | The matter pressures you — hardest case |

Read the ladder by stage: **用卦 is the present situation, 互卦 the process, 变卦 the outcome direction.** Weigh 用卦 first, let the 变卦 entries tip the direction, use 互卦 to shade the middle passage. The output contract is unchanged: two layers (inner 体用要点 / outer plain conclusion) and the `result.canonicalUrl` link at the end.

## Output

Two layers (see SKILL.md — the plain layer is mandatory):

**Inner layer (卦象要点 — for traceability, compact, terms OK):**

1. **卦象概览** — hexagram name + the core message of 卦辞
2. **动爻解读** — what the changing lines specifically say (if any)
3. **变卦趋势** — the outcome direction (if there are changing lines)

**Outer layer (大白话结论 — for the user, always last, no raw jargon):**

4. **一句话回答你的问题** — direct answer to the user's actual question, in their own words. Yes/no + a short why. E.g. "该去。这卦整体是通的，越走越开，主要卡点在第 4 个月前后，扛过去就顺了。"
5. **接下来具体怎么做** — 2-3 concrete actions derived from the 贞悔亨厉 verdict, in plain verbs ("现在就可以推进", "再等一个月看看", "先别签"). No "贞/悔/吝/厉" in this layer unless you've already glossed it.

**Canonical Link (出处链接，必须附在末尾):**
Append the `result.canonicalUrl` (e.g. `https://eastalmanac.com/yijing/22/4`) at the end for the user to view the full hexagram diagram and commentaries.

For date-selection (择日) and specific event consultation, route to the **date-selection** reference which builds on this divination.
