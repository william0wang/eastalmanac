# EastAlmanac Liu Yao Najia Chart (六爻排盘) — Data Layer

This skill installs a full **six-line Najia chart** (六爻纳甲排盘) and reads it structurally. Use it when the user asks for 六爻/纳甲/排盘 explicitly, or when one concrete matter needs the deeper classical machinery — 卦宫 (palace), 六亲 (six relations), 六神 (six spirits), 世应 (self/other seats), 伏神 (hidden spirits) — beyond a plain I Ching cast. For a quick single-decision reading, a plain cast (**yijing-cast**) is often enough; 六爻 pays off when the question involves other parties, money, or timing ("这次合作能成吗", "这次面试有戏吗", "对方是什么意思").

For term definitions (六亲/六神/世应/伏神), consult **glossary**; this file covers the tool contract and the reading order.

## Core Principle — The Diviner Must Cast

Same hard rule as **yijing-cast**: the chart is only meaningful when the **user personally** draws it. On the liuyao page the user draws **six strokes** (one per line, bottom to top); each stroke lands as one of the four states — 少阴 / 少阳 (static) or 老阴 / 老阳 (moving). NEVER generate, guess, or auto-fill the strokes.

The engine takes the **day stem** (日干, from the user's local date at draw time); it fixes the 六神 start and is returned in `dayStem`. Use it when weighing 日辰生克.

## Step 0 — Gather the Question

Same as **yijing-cast** Step 0: one specific real-life question in the user's own words. A vague "帮我排个卦" needs narrowing first — frame it as their concrete matter, not a menu.

## Step 1 — Install the Chart via Interactive Bridge

```bash
python3 scripts/bridge.py liuyao --question="用户所问之事" --lang=<locale>
```

`--lang=en|zh|zh-tw|es|pt|de|ja` (default `en`) picks the page locale; tool labels and the returned `prompt` follow it. The bridge opens `https://eastalmanac.com/tools/liuyao/` (locale-prefixed) where the user draws the six strokes; the chart installs automatically after the sixth. Clicking **「⚡ 回传给终端 Agent」** posts the structured payload back.

**Direct Input / Clipboard Recognition**: as with every action, if the user pastes an EastAlmanac liuyao result (or a `/r/l.301201.0` share permalink from the page), work from it directly without launching the browser.

### Return Data Structure

```json
{
  "version": "1.0",
  "source": "eastalmanac.com",
  "action": "liuyao",
  "input": {
    "question": "这次合作能成吗？",
    "strokes": [3, 0, 1, 2, 0, 1],
    "dayStem": "甲"
  },
  "result": {
    "benGua": { "name": "贲", "binary": 37 },
    "palace": "艮土",
    "member": "一世卦",
    "dayStem": "甲",
    "lines": [
      { "spirit": "青龙", "najia": "己卯木", "relation": "官鬼", "moving": true,  "shi": true,  "ying": false, "hidden": null },
      { "spirit": "朱雀", "najia": "己丑土", "relation": "兄弟", "moving": false, "shi": false, "ying": false, "hidden": "父母丙午" },
      { "spirit": "勾陈", "najia": "己亥水", "relation": "妻财", "moving": false, "shi": false, "ying": false, "hidden": "子孙丙申" },
      { "spirit": "腾蛇", "najia": "丙戌土", "relation": "兄弟", "moving": true,  "shi": false, "ying": true,  "hidden": null },
      { "spirit": "白虎", "najia": "丙子水", "relation": "妻财", "moving": false, "shi": false, "ying": false, "hidden": null },
      { "spirit": "玄武", "najia": "丙寅木", "relation": "官鬼", "moving": false, "shi": false, "ying": false, "hidden": null }
    ],
    "bianGua": "旅",
    "canonicalUrl": "https://eastalmanac.com/tools/liuyao/",
    "shareUrl": "https://eastalmanac.com/r/l.301201.0"
  },
  "prompt": "六爻两层解读提示词（用神/世应/动爻/变卦与出处）",
  "question": "这次合作能成吗？",
  "syncedAt": "2026-10-13T12:00:00.000Z"
}
```

### Result fields

`lines` is **bottom → top**: index 0 = 初爻, index 5 = 上爻 (the page renders 上爻 first; the payload keeps cast order, same as `strokes`).

| Field | What it contains | How to use it |
| ----- | --------------- | ------------- |
| `input.strokes` | The six states the user drew, each 0–3 | 0 = 少阴, 1 = 少阳, 2 = 老阴 (moving yin), 3 = 老阳 (moving yang) |
| `benGua` | Primary hexagram name + 6-bit binary (bit i = line i, bottom = 0) | The chart being read |
| `palace` | 卦宫 + its element (e.g. 艮土) | The "self" element every 六亲 is judged against |
| `member` | Palace membership: 本卦 / 一世卦 … 五世卦 / 游魂卦 / 归魂卦 | Locates the hexagram in its palace |
| `dayStem` | Day stem at draw time (e.g. 甲) | ① Fixed the 六神 start (甲乙青龙起初爻, 丙丁朱雀, 戊勾陈, 己腾蛇, 庚辛白虎, 壬癸玄武, then sequentially upward); ② the 日辰 for weighing 用神旺衰 |
| `lines[].spirit` | 六神 of that line | Color, not verdict: 青龙 吉庆 / 朱雀 口舌文书 / 勾陈 田土迟滞 / 腾蛇 虚惊怪异 / 白虎 凶伤病灾 / 玄武 暗昧失脱 |
| `lines[].najia` | 纳甲: stem + branch + branch element (e.g. 己卯木) | The line's 干支; the branch element feeds all 生克 judgments |
| `lines[].relation` | 六亲 vs the palace element | The casting vocabulary — 兄弟 / 子孙 / 妻财 / 官鬼 / 父母 |
| `lines[].moving` | True on 老阴/老阳 lines | Moving lines are the engine of the reading |
| `lines[].shi` / `ying` | 世 / 应 seat (at most one of each) | 世 = the querent's side; 应 = the other party |
| `lines[].hidden` | 伏神 under this line, null if none | The palace-head line absent from 本卦; fallback 用神 source when its 六亲 is missing from the visible lines |
| `bianGua` | Transformed hexagram (present iff any line is moving) | Where the matter trends |
| `shareUrl` | Per-cast permalink (`/r/l.<strokes>.<dayStem>`) | Opens this exact chart as a static page — the reference link to append for the user |
| `canonicalUrl` | The tool page (locale-prefixed) | General source link |

## Step 2 — Structural Reading

The site has installed the full chart; the judgment is yours. Read in this order (classical 用神-first school):

### 1. 取用神 — pick the Useful Spirit by question category

The 六亲 that *is* the matter:

| Question about | 用神 |
| -------------- | ---- |
| Self — own fortune, health, state of mind | 世爻 |
| Love/marriage — asked by a woman / by a man | 官鬼 / 妻财 |
| Illness — the affliction / the cure | 官鬼 (病) / 子孙 (药) |
| Career, position, lawsuits | 官鬼 |
| Money, deals, trading | 妻财 |
| Parents, elders, homes, documents, contracts, exams | 父母 |
| Children, juniors, pets | 子孙 |
| Siblings, friends, peers, rivals | 兄弟 |

If the chosen 用神 does not appear among `lines[].relation`, look for it in `lines[].hidden` (伏神) — traditionally weaker until a moving line draws it out or its day arrives.

### 2. 旺衰 — weigh 用神 against the day and the moving lines

Compare 用神's branch element with the day stem's element (日辰生扶 or 克制) and with every moving line (动爻生用神 = support; 动爻克用神 = pressure), and note whether 用神 itself sits on a moving line (the matter is already in motion). The payload carries the day stem but not the month branch — derive 月建 from `syncedAt` only if you can do it reliably; otherwise weigh the day and the moving lines, and don't invent the month.

### 3. 世应 — self vs the other party

世 vs 应: their najia branches 合 (cooperation), 冲 (friction), or element 生克 sets the two-party baseline — decisive in partnerships, negotiations, interviews.

### 4. 动爻 — what is moving, and where it pushes

Each moving line pushes its 六亲 agenda along the element chain (e.g. 妻财动生官鬼 — money moving feeds the position; 兄弟动克妻财 — rivals eat the money). Follow the moving lines' branches to who generates whom.

### 5. 变卦 — the trend

`bianGua` shows the direction; a moving line transforming into support (化进/化生) strengthens, transforming into drain (化退/化绝) weakens.

**Verdict shaping**: synthesize 1–5 into a directional verdict — 可成 / 难成 / 有变数 / 时机未到 — plus where the pivot sits. Moving lines' branches give timing hints (应期 often at the branch's 冲 or 合 day); state timing only when honestly derivable, as a tendency, never a certainty.

## Output

Two layers (see SKILL.md — the plain layer is mandatory and always last):

**Inner layer (卦象要点 — compact, terms OK after gloss):**

1. **卦象概览** — 本卦 (palace + membership) → 变卦, day stem, one-line setup
2. **用神与旺衰** — which 用神, its najia, day/moving-line support or pressure
3. **世应与动爻** — the parties' baseline + what the moving lines push
4. **应期与变数** — likely timing pivot (if honestly derivable) + the swing factor

**Outer layer (大白话结论 — always last, no raw jargon):**

5. **一句话回答** — direct answer to the user's actual question (成不成 / 该不该 / 何时动)
6. **接下来怎么做** — 2–3 concrete plain-verb next steps tied to the verdict (推进 / 等待 / 补条件 / 避风险)

**Canonical Link (附在末尾):** append `result.shareUrl` (the per-cast permalink, e.g. `https://eastalmanac.com/r/l.301201.0`) so the user can reopen the exact chart.

## Related

- Quick single-decision casting without the Najia machinery → **yijing-cast** (`bridge.py cast`; the same page also hosts Meihua 梅花体用 behind its method selector — the returned `input.method` says which reading came back)
- Choosing an auspicious date once the matter is decided → **date-selection** (`bridge.py dates`)
