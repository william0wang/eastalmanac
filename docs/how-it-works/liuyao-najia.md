# The Liu Yao Najia Chart: Jing Fang's Eight Palaces, Stem-Branch Assignment, and the Six Relations

_Last verified: 2026-10_

## TL;DR
Liu Yao (六爻纳甲) is the deepest of the three I Ching methods on EastAlmanac: a full classical divination board installed from six hand-drawn strokes. The engine is **pure and table-driven** — zero randomness, zero clock. Each stroke yields one number; `number mod 8` maps it to one of the four line images (老阴/少阳/少阴/老阳) at exact three-coin probabilities. Six line states plus the **day stem (日干)** then install the complete Jing Fang (京房) board: the hexagram's palace (八宫) and member generation, a stem-branch pair (纳甲) on every line, the six relations (六亲) judged against the palace element, the six spirits (六神) rotating from the day stem, the self/other seats (世应), hidden spirits (伏神) where a relation is missing, and the transformed hexagram (变卦) when lines move.

---

## 1. Core Principle: The Six Strokes Are the Oracle

The liuyao page asks the user to draw **six freehand strokes** (bottom to top, one per line). Each stroke is a conscious act — the hand position plays the role of the tossed coins. The stroke sampler folds the drawn geometry into a number (`numberFromStroke`); there is deliberately **no `Math.random()` and no clock seed** anywhere in the chain.

```text
six strokes → six numbers (bottom→top) → six line states → + day stem → full Najia board
```

---

## 2. From Stroke Number to Line State: mod 8

`numberToSiXiang(strokeNumber)` inspects `((strokeNumber mod 8) + 8) mod 8` — the wrapped residue, so negative numbers behave identically:

| Residue | Line image | Polarity | Changing? | Coin-toss analogue | Probability |
|---|---|---|---|---|---|
| 0 | 老阴 Old Yin | Yin | **Yes** | 3 tails (value 6) | 1/8 |
| 1–3 | 少阳 Young Yang | Yang | No | 2 tails 1 head (7) | 3/8 |
| 4–6 | 少阴 Young Yin | Yin | No | 1 tail 2 heads (8) | 3/8 |
| 7 | 老阳 Old Yang | Yang | **Yes** | 3 heads (9) | 1/8 |

Exactly six numbers are required — `numbersToLineStates` rejects any other count.

---

## 3. The Eight Palaces (京房八宫) — How a Hexagram Finds Its Home

Every one of the 64 hexagrams belongs to exactly one palace, generated from the palace's **pure hexagram (八纯卦)** by the classical line-flipping sequence. Palace order: 乾 坎 艮 震 巽 离 坤 兑.

| Member | Lines flipped from the palace head (0-indexed) | 世 seat (1-indexed) |
|---|---|---|
| 本卦 (head) | none | 6 |
| 一世卦 | [0] | 1 |
| 二世卦 | [0,1] | 2 |
| 三世卦 | [0,1,2] | 3 |
| 四世卦 | [0,1,2,3] | 4 |
| 五世卦 | [0,1,2,3,4] | 5 |
| 游魂卦 | [0,1,2,4] — line 4 (index 3) restored | 4 |
| 归魂卦 | [4] — inner trigram restored | 3 |

Reading the flip lists cumulatively: 一世 flips line 1; 二世 keeps that and adds line 2; …五世 has lines 1–5 flipped. 游魂 then **restores line 4** (keeps 1,2,3,5 flipped), and 归魂 **restores the whole inner trigram** (only line 5 stays flipped).

**世应 (self/other seats)**: the 世 (self) line is fixed per member — `[6,1,2,3,4,5,4,3]` (1-indexed) — and 应 (the other party) always sits **three lines apart**: `yingSeat = ((shiSeat - 1 + 3) mod 6) + 1`, i.e. 1↔4, 2↔5, 3↔6 (the engine computes the same thing 0-indexed: `(shi + 3) % 6`).

---

## 4. Najia (纳甲): a Stem-Branch Pair on Every Line

Each trigram carries stem assignments (inner = lower position, outer = upper) and branch sequences (bottom→top within the trigram):

| Trigram | Element | Inner stem | Outer stem | Inner branches | Outer branches |
|---|---|---|---|---|---|
| 乾 | 金 | 甲 | 壬 | 子 寅 辰 | 午 申 戌 |
| 坎 | 水 | 戊 | 戊 | 寅 辰 午 | 申 戌 子 |
| 艮 | 土 | 丙 | 丙 | 辰 午 申 | 戌 子 寅 |
| 震 | 木 | 庚 | 庚 | 子 寅 辰 | 午 申 戌 |
| 巽 | 木 | 辛 | 辛 | 丑 亥 酉 | 未 巳 卯 |
| 离 | 火 | 己 | 己 | 卯 丑 亥 | 酉 未 巳 |
| 坤 | 土 | 乙 | 癸 | 未 巳 卯 | 丑 亥 酉 |
| 兑 | 金 | 丁 | 丁 | 巳 卯 丑 | 亥 酉 未 |

Classical mnemonic: 乾纳甲壬、坤纳乙癸、艮丙、兑丁、坎戊、离己、震庚、巽辛. The lower trigram of the cast hexagram is read from the Inner columns, the upper from the Outer columns — six `stem+branch` pairs, one per line, bottom to top.

Branch elements follow the standard map: 申酉金、寅卯木、子亥水、巳午火、辰戌丑未土.

---

## 5. The Six Relations (六亲) and Hidden Spirits (伏神)

Six relations are judged with the **palace element as "me" (我)**:

| Relation | Rule against palaceElement | Reads as |
|---|---|---|
| 兄弟 | line element = palace element | peers, rivals, siblings |
| 子孙 | palace generates line | output, ease, descendants |
| 父母 | line generates palace | support, documents, elders |
| 妻财 | palace overcomes line | money, assets, (spouse in classical framing) |
| 官鬼 | line overcomes palace | pressure, authority, illness |

**Hidden spirits (伏神)**: a hexagram may show only four of the five relations. For each line, if the palace-head hexagram's line at the **same position** carries a relation absent from this hexagram, that assignment is reported as a hidden spirit under the line. Palace heads themselves are complete — they never carry hidden spirits.

---

## 6. The Six Spirits (六神) — Rotating from the Day Stem

The day stem (日干 of the drawing day) fixes which spirit starts at line 1 (bottom); the remaining five follow in fixed order 青龙 → 朱雀 → 勾陈 → 腾蛇 → 白虎 → 玄武, wrapping cyclically upward.

| Day stem | Spirit on line 1 |
|---|---|
| 甲 / 乙 | 青龙 |
| 丙 / 丁 | 朱雀 |
| 戊 | 勾陈 |
| 己 | 腾蛇 |
| 庚 / 辛 | 白虎 |
| 壬 / 癸 | 玄武 |

---

## 7. The Transformed Hexagram (变卦)

Lines marked 老阴 or 老阳 are changing: the transformed hexagram flips every changing line's polarity. The engine reports the transformed hexagram's **binary and King Wen name only** — it deliberately does *not* install a second Najia board for it; deep readings treat the transformed hexagram by its own identity.

---

## 8. Worked Golden Examples

### Example 1: 乾为天 (all six yang, static) — full board, day stem 甲

Lines bottom→top: 甲子·子孙·青龙, 甲寅·妻财·朱雀, 甲辰·父母·勾陈, 壬午·官鬼·腾蛇, 壬申·兄弟·白虎, 壬戌·父母·玄武.

- Palace 乾 (金), member 本卦 → **世 on line 6 (top), 应 on line 3**
- All five relations appear (a complete palace head — no hidden spirits)
- No line changes → `bianGua` is null

### Example 2: 天风姤 — one-generation member of 乾宫, with a hidden spirit

Cast lines (bottom→top): 0,1,1,1,1,1 → 姤, 乾宫一世卦, **世 on line 1, 应 on line 4**.

- Lower trigram 巽 (辛): line 1 辛丑·父母, line 2 辛亥·子孙, line 3 辛酉·兄弟
- Upper trigram 乾 (壬): line 4 壬午·官鬼, line 5 壬申·兄弟, line 6 壬戌·父母
- 妻财 is missing from the board → the palace head's line 2 (甲寅·木) is reported as a **hidden spirit under line 2**, the only one on the chart

### Example 3: Six spirits rotate with the day stem (乾, static)

| Day stem | Spirits bottom→top |
|---|---|
| 癸 | 玄武 青龙 朱雀 勾陈 腾蛇 白虎 |
| 庚 | 白虎 玄武 青龙 朱雀 勾陈 腾蛇 |
| 戊 | 勾陈 腾蛇 白虎 玄武 青龙 朱雀 |

### Example 4: Changing lines flip

- 乾 with line 1 as 老阳 → transformed hexagram **姤** (`0b111110`)
- A cast with 老阳 at line 1 and 老阴 at line 4 (`0b100101`) flips both → **旅** (`0b101100`)

---

## 9. Engine Invariants (all 64 hexagrams, machine-checked)

The test suite installs every binary 0–63 and asserts: each palace hosts **exactly 8** members; each palace carries **all 8 member kinds** exactly once; 世/应 are always a unique pair exactly **three lines apart**; the six relations **plus hidden spirits always cover all five** relations; palace heads carry **no** hidden spirits.

---

## Try It Online
Draw the six strokes yourself and watch the board install:
- **Liu Yao Najia Tool**: [https://eastalmanac.com/tools/liuyao/](https://eastalmanac.com/tools/liuyao/)
