# The Mathematics of Three-Number I Ching Casting: Bitwise State Machines and Changing Line Logic

_Last verified: 2026-10_

## TL;DR
In ancient divination, the consultation of the *I Ching* (Book of Changes, 易经) required forty-nine yarrow stalks or three tossed bronze coins to capture the synchronicity of the moment. EastAlmanac adapts this into a deterministic, computer-aided casting engine: the seeker **draws strokes on a canvas**, the engine folds the drawing into **three numbers between 0 and 99**, and blends the drawing moment into the coin bits. The engine contains **zero random number generators (`Math.random()`) and zero system clock seeds**—the numbers must originate entirely from the seeker's strokes and their moment. Using 3-bit modulo arithmetic, the engine derives all six lines, detects changing lines (动爻), computes the transformed hexagram (之卦), and selects the authoritative judgment according to Master Zhu Xi's classical rules.

---

## 1. Core Principle: Zero Algorithmic Randomness

Most divination websites use `Math.random()` to generate hexagrams behind the scenes. In classical metaphysics, this destroys the integrity of the oracle:
- **Synchronicity (感应)**: Divination is not noise generation; it is a synchronistic interface connecting the seeker's subjective consciousness with objective reality.
- **The Seeker Must Cast**: If the server invents the numbers, the machine is querying itself.
- **EastAlmanac Contract**: The engine accepts exactly three integers (`firstNumber`, `secondNumber`, `thirdNumber`), each in the range 0–99. If the caller does not supply them, casting fails immediately.

---

## 2. Where the Three Numbers Come From: Stroke Folding + the Moment Blend

On the cast page the seeker draws strokes; the engine derives the three numbers in two pure steps:

1. **Stroke folding** (`stroke.ts`): the sampled stroke geometry is folded by three independent FNV-style hash accumulators into three numbers, each 0–99. The hand shapes the numbers; there is no clock and no randomness.
2. **Moment blend** (`coin-moment.ts`): at pointer-up the page passes the drawing moment (`momentMs`) as an explicit parameter, and the engine re-decides only the **three coin bits** — the low 3 bits of each number:

```text
coinBits    = (strokeNumber XOR hashMoment(momentMs, index)) AND 0b111
blendedNumber = (strokeNumber AND ~0b111) OR coinBits
```

`hashMoment` is a deterministic 32-bit FNV-1a mix (seed `0x9e3779b9`) finalized with a Wang avalanche step. The semantics are the classical one: **the high bits keep the stroke (the hand shapes the cast); the low 3 bits are the three coins, and the moment decides which face each coin lands on.** Same stroke + same moment → the same cast forever; same stroke in another moment → different coins. This restores the original app's behavior, where every coin bit was reseeded from the moment — the moment is part of the 机锋.

**Golden fixtures** (pinned; a 4-point stroke folds to `[20, 55, 21]`):

| Input | Result |
|---|---|
| strokeNumber `[20, 55, 21]`, `momentMs = 0` | `[22, 54, 18]` |
| same stroke, `momentMs = 1760000000000` | `[23, 50, 23]` |
| same stroke, `momentMs = 1760000001000` | `[18, 50, 21]` |

Note how only the low 3 bits move (20 = `0b10100` → 22 = `0b10110`; 55 = `0b110111` → 54 = `0b110110`) — the stroke stays in the number.

---

## 3. Deriving Six Lines via 3-Bit Modulo Arithmetic

Each integer produces a pair of consecutive lines, mapping the three inputs into the six lines of the hexagram (from bottom 初爻 to top 上爻):
- `firstNumber` yields **Line 0** (`intToYao(firstNumber)`) and **Line 1** (`intToYao(firstNumber + 1)`)
- `secondNumber` yields **Line 2** (`intToYao(secondNumber)`) and **Line 3** (`intToYao(secondNumber + 1)`)
- `thirdNumber` yields **Line 4** (`intToYao(thirdNumber)`) and **Line 5** (`intToYao(thirdNumber + 1)`)

### The `intToYao` Function
To determine whether a line is Yin, Yang, or Changing, the engine examines the lowest 3 bits of the number (`number mod 8`) and counts the active `1` bits (`bitCount`):

| Active 1 Bits (`bitCount`) | Binary State | Classical State | Line Polarity | Changing? |
|---|---|---|---|---|
| **`bitCount = 0`** (all 0s) | `0b10` | **Old Yin (老阴 / 阴动)** | Yin ($--$) | **Yes (Changing)** |
| **`bitCount = 1`** (single 1) | `0b01` | **Young Yang (少阳 / 静阳)** | Yang (—) | No (Static) |
| **`bitCount = 2`** (two 1s) | `0b00` | **Young Yin (少阴 / 静阴)** | Yin ($--$) | No (Static) |
| **`bitCount = 3`** (all 1s) | `0b11` | **Old Yang (老阳 / 阳动)** | Yang (—) | **Yes (Changing)** |

### Mathematical Equivalence to Coin Tossing (三铜钱法)
Notice how this bitwise mapping mirrors the classical coin method:
- 3 Tails $\rightarrow$ Value 6 (Old Yin, Changing)
- 2 Tails, 1 Head $\rightarrow$ Value 7 (Young Yang, Static)
- 1 Tail, 2 Heads $\rightarrow$ Value 8 (Young Yin, Static)
- 3 Heads $\rightarrow$ Value 9 (Old Yang, Changing)

By evaluating the parity and Hamming weight of the 3-bit register, the algorithm preserves the exact fourfold states of the lines.

---

## 4. Hexagram Structures: Ben Gua, Dong Yao, and Zhi Gua

1. **Original Hexagram (Ben Gua, 本卦)**:
   Formed by stacking the base polarity (bit 0) of the six lines from bottom (Line 0) to top (Line 5).
2. **Changing Lines (Dong Yao, 动爻)**:
   Any line with bit 1 active (`0b10` or `0b11`) is an unstable, mutating line representing dynamic shifts in the situation.
3. **Transformed Hexagram (Zhi Gua, 之卦)**:
   Formed by flipping the polarity of every changing line (Old Yin becomes Yang; Old Yang becomes Yin), revealing the future trajectory.

---

## 5. Master Zhu Xi's Changing Line Judgment Rules

When multiple lines change, which text governs the reading? EastAlmanac implements the authoritative hierarchical rules codified by Master Zhu Xi (朱熹) and Jiao Yanshou (焦延寿):

| Number of Changing Lines | Governing Judgment Text | Metaphysical Rationale |
|---|---|---|
| **0 lines change** | **Primary Hexagram Statement (本卦卦辞/彖辞)** | The situation is stable and holistic; evaluate the overall symbol. |
| **1 line changes** | **The Changing Line Text (动爻爻辞)** | The mutation is focused entirely on a single focal point. |
| **2 lines change** | **The Yin Changing Line (or Upper Line)** | If one line is Yin and one is Yang, read the Yin line (Yin seeks Yang). If both are identical polarity, read the upper changing line. |
| **3 lines change** | **The Middle Changing Line** | Three changing lines divide the hexagram in half; the middle changing line represents the turning pivot. |
| **4 lines change** | **The Lower of the Two Static Lines (下静爻)** | When momentum is overwhelmingly in flux, guidance rests in stability. Read the lower static line in the Transformed Hexagram. |
| **5 lines change** | **The Single Static Line (唯一静爻)** | The lone static line anchors the entire transformed state. |
| **6 lines change** | **Use Nine / Use Six, or Transformed Hexagram** | For Hexagram 1 (Qian): Read **Use Nine (用九)**. For Hexagram 2 (Kun): Read **Use Six (用六)**. For all other 62 hexagrams: Read the **Judgment of the Transformed Hexagram (之卦卦辞/彖传)**. |

---

## 6. Worked Golden Examples

### Example 1: Numbers `[7, 23, 41]`
- `firstNumber = 7`:
  - 7 = `0b111` → `bitCount = 3` → **Line 0: Old Yang** (`0b11`, Changing Yang)
  - 8 = `0b000` (8 mod 8 = 0) → `bitCount = 0` → **Line 1: Old Yin** (`0b10`, Changing Yin)
- `secondNumber = 23`:
  - 23 = `0b111` (23 mod 8 = 7) → `bitCount = 3` → **Line 2: Old Yang** (`0b11`, Changing Yang)
  - 24 = `0b000` (24 mod 8 = 0) → `bitCount = 0` → **Line 3: Old Yin** (`0b10`, Changing Yin)
- `thirdNumber = 41`:
  - 41 = `0b001` (41 mod 8 = 1) → `bitCount = 1` → **Line 4: Young Yang** (`0b01`, Static Yang)
  - 42 = `0b010` (42 mod 8 = 2) → `bitCount = 1` → **Line 5: Young Yang** (`0b01`, Static Yang)

**Results**:
- **Lines (Bottom $\rightarrow$ Top)**: Yang (Chg), Yin (Chg), Yang (Chg), Yin (Chg), Yang, Yang
- **Primary Hexagram**: Hexagram 37 — **Jia Ren (家人 / The Family)**
- **Changing Lines**: 4 lines change (Lines 0, 1, 2, 3)
- **Judgment Selection**: Per the 4-line rule, read the lower static line (Line 4) of the Transformed Hexagram.

---

### Example 2: Numbers `[0, 1, 6]`
- 0 = `0b000` → `bitCount = 0` → Line 0: Old Yin (`0b10`, Changing Yin)
- 1 = `0b001` → `bitCount = 1` → Line 1: Young Yang (`0b01`, Static Yang)
- 1 = `0b001` → `bitCount = 1` → Line 2: Young Yang (`0b01`, Static Yang)
- 2 = `0b010` → `bitCount = 1` → Line 3: Young Yang (`0b01`, Static Yang)
- 6 = `0b110` → `bitCount = 2` → Line 4: Young Yin (`0b00`, Static Yin)
- 7 = `0b111` → `bitCount = 3` → Line 5: Old Yang (`0b11`, Changing Yang)

**Results**:
- **Primary Hexagram**: Hexagram 50 — **Ding (鼎 / The Cauldron)**
- **Changing Lines**: 2 lines change (Line 0 and Line 5).
- **Judgment Selection**: Line 0 is Yin, Line 5 is Yang $\rightarrow$ prioritized reading on **Line 0 (初六)**.

---

## Try It Online
Cast your own three numbers and explore the dynamic line commentary:
- **Interactive I Ching Casting Tool**: [https://eastalmanac.com/tools/cast/](https://eastalmanac.com/tools/cast/)
