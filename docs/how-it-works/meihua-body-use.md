# Meihua Body-Use Analysis: One Hexagram, the Five-Element Reading

_Last verified: 2026-10_

## TL;DR
Meihua (梅花易数) is the second I Ching method on EastAlmanac — and the deepest design decision is what it **shares** with the coin oracle: the *same* strokes, the *same* drawing moment, the *same* three numbers, the *same* hexagram. It differs only in the reading frame. Instead of quoting the changing line's classical text, it reads the **five-element interaction between the two trigrams** — the classical 体用总诀 (body-use formula). The engine splits the hexagram into a body trigram (体) and a use trigram (用), computes the nuclear trigrams (互卦), and grades every frame — use, nuclear, transformed — against the body on a five-step verdict scale. Pure functions all the way down; the panel is deterministic for a given cast.

---

## 1. One Cast, Two Readings

The cast page hosts both methods behind a selector. The derivation chain (strokes → three numbers → six lines → Ben Gua / changing lines / Zhi Gua) is **computed once and shared**. The returned payload marks which reading you got:

| `input.method` | Reading frame |
|---|---|
| `"coin"` | Classical text of the changing line (Zhu Xi rules) |
| `"meihua"` | Five-element body-use panel (`result.tiYong`) |

## 2. Splitting Body and Use (体用) — the Pinned Rule

A coin cast can move **multiple** lines — the classical Meihua time-cast (年月日时起卦) never could. So the engine pins ONE deterministic assignment:

1. **Use (用) = the trigram containing the changing lines**; the quiet trigram is the body (体).
2. **Both trigrams moving** → the one with **more** changing lines is the use; a **tie goes to the upper** trigram (`useIsUpper = changingUpper >= changingLower`).
3. **Fully static cast** → no body/use split exists: `ti` and `yong` are `null`, and the hexagram judgment (卦辞) stays the whole reading — exactly how the coin method reads it.

**Where each rule comes from**: rule 1 is the classical text verbatim — 「凡上下二卦无动爻者为体，有动爻者为用」(《梅花易数》). But a classical time-cast (年月日时起卦) always yields exactly ONE moving line, so rules 2–3 have no classical precedent either way; published schools that handle multi-moving coin casts pick the first or lowest moving line (or a 世爻-based tie-break, itself marked 非古法). This engine's "more movement wins, tie → upper" is therefore a published implementation convention — deterministic, and identical to the classical rule in the single-moving-line case the classics actually cover.

Each trigram carries its identity (name + element) from the standard eight-trigram table: 乾金 坤土 震木 巽木 坎水 离火 艮土 兑金.

## 3. The Nuclear Trigrams (互卦)

The nuclear hexagram re-reads the middle of the situation — lines 2–4 (1-indexed) as its lower trigram, lines 3–5 as its upper. It is itself a full hexagram, named by its King Wen number. The panel reports its name plus the two trigram identities.

## 4. The Five Verdicts (体用总诀)

Every frame — use trigram, each nuclear trigram, each transformed trigram — is graded by how its element acts on the **body element**:

| Relation | Direction | Verdict | One-line meaning |
|---|---|---|---|
| 生体 | frame generates body | `auspicious` 大吉 | The situation feeds you |
| 体克 | body overcomes frame | `auspicious` 小吉 | You control the situation |
| 比和 | same element | `harmony` 吉 | Smooth fit, low friction |
| 体生 | body generates frame | `draining` 耗泄 | You spend yourself into it |
| 克体 | frame overcomes body | `controlled` 受制 | The situation pressures you |

The `ladder` array carries the frames **in reading order** — use trigram first (the present), then upper and lower nuclear trigrams (the process), then the transformed hexagram's upper and lower trigrams (where it heads) — each as `frame·label:relation`.

## 5. Worked Golden Example — the same `[7, 23, 41]` family cast

Take the exact cast documented in the three-number casting article: numbers `[7, 23, 41]` → **Jia Ren 家人** (lower 离 Fire, upper 巽 Wood), changing lines 1–4 (bottom four), lines 5–6 static.

**Body/use split** — lower trigram holds 3 changing lines, upper holds 1 → more movement wins → **用 = lower 离火 (Fire), 体 = upper 巽木 (Wood)**.

**Nuclear trigrams** — lines 2–4 = 阴阳阴 = 坎 (Water), lines 3–5 = 阳阴阳 = 离 (Fire) → nuclear hexagram 未济.

**Transformed hexagram** — flipping lines 1–4 gives lower 坎 / upper 乾 → 讼 (King Wen 6).

**The ladder** (body element = 木 Wood):

| Frame | Element | Acts on 木 | Relation |
|---|---|---|---|
| 用卦 离 | Fire | wood feeds fire | 体生 (draining) |
| 互卦 上互·离 | Fire | wood feeds fire | 体生 (draining) |
| 互卦 下互·坎 | Water | water grows wood | 生体 (auspicious) |
| 变卦 乾 | Metal | metal chops wood | 克体 (controlled) |
| 变卦 坎 | Water | water grows wood | 生体 (auspicious) |

Reading it by stage: the matter itself drains you (用泄体), the middle passage starts costly but turns nourishing (互卦先泄后滋), and the outcome direction mixes pressure with support (变卦先克后生). A human diviner would call this: **the affair takes real effort, gains help mid-way, and lands with costs partly recovered — not a clean win, far from a loss.**

## 6. Boundary Cases

- **Static cast**: `ti`/`yong` null, `targets` empty — read the 卦辞, as the coin method does.
- **All six lines moving**: the engine deliberately reports the transformed code as the Ben Gua (之卦彖传 reading) — the panel gates on line movement, never on `zhiGuaCode ≠ benGuaCode`.
- **Tie in movement**: upper trigram becomes the use.

---

## Try It Online
Pick 梅花易数 in the cast page's method selector and draw:
- **I Ching Casting Tool (Meihua behind the method selector)**: [https://eastalmanac.com/tools/cast/](https://eastalmanac.com/tools/cast/)
