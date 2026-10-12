# How BaZi Four Pillars Are Cast: Wall-Clock Authority, Sects, and Decade Cycles

_Last verified: 2026-10_

## TL;DR
BaZi (Four Pillars of Destiny, 八字) translates a person's birth moment into four sexagenary pillar pairs (Year, Month, Day, Hour). Unlike modern calendar systems, BaZi is fundamentally solar-astronomical: the year begins at Lichun (立春, Solar Term 315°), months change at the entry of the 12 Jie (节) solar terms, and hours follow local two-hour double-hour increments. EastAlmanac enforces a strict **Birthplace Wall-Clock Authority** rule (ignoring misleading UTC conversions), defaults to **Sect 2 (子初换日)** for late-night births, and calculates exact decade fortunes (大运) using classical day-to-year solar-term distance algorithms.

---

## 1. The Timezone Contract: Birthplace Wall-Clock Authority

Modern developers often default to ISO 8601 UTC timestamps (e.g., `1990-01-15T14:30:00Z`). In Chinese metaphysics, this is a dangerous pitfall:
1. **Solar Terms Are Geocentric Coordinates**: Solar terms represent the sun's exact ecliptic longitude. They are celestial events, not administrative timezone shifts.
2. **Local True Solar Clock**: The human body experiences night, dawn, noon, and dusk according to the sun directly overhead at the place of birth. A birth occurring at 23:30 in New York should not be translated to 04:30 UTC next day in London, because the physical birth occurred in the deep night of North America.

### The Contract
- **Input**: The wall-clock datetime recorded at the place of birth (`YYYY-MM-DD HH:MM:SS`).
- **Trailing Offsets**: If an explicit offset (e.g., `+08:00` or `Z`) is present, our parser validates the format and then **intentionally strips and ignores it**.
- **No `new Date()` Conversions**: The engine parses date fields via pure integer arithmetic. It never relies on system host runtime clocks or browser local timezones, ensuring 100% deterministic output on servers in any part of the world.

---

## 2. Astronomical Boundaries and School Choices

### A. The Month Boundary: Solar Terms (节气), Never Calendar Months
A common misconception is that the BaZi month changes on the 1st of the Gregorian or Lunar month. In reality:
- Month stems and branches change **the precise minute the sun enters the governing Solar Term (节)**:
  - 1st Month (寅 Yin): Lichun (立春)
  - 2nd Month (卯 Mao): Jingzhe (惊蛰)
  - 3rd Month (辰 Chen): Qingming (清明)
  - 4th Month (巳 Si): Lixia (立夏)
  - 5th Month (午 Wu): Mangzhong (芒种)
  - 6th Month (未 Wei): Xiaoshu (小暑)
  - 7th Month (申 Shen): Liqiu (立秋)
  - 8th Month (酉 You): Bailu (白露)
  - 9th Month (戌 Xu): Hanlu (寒露)
  - 10th Month (亥 Hai): Lidong (立冬)
  - 11th Month (子 Zi): Daxue (大雪)
  - 12th Month (丑 Chou): Xiaohan (小寒)

If a child is born on February 3rd before the exact moment of Lichun, they belong to the previous year's 12th month (Chou month), not the new year.

---

### B. The Zi Hour Dilemma: Sect 1 vs. Sect 2 (早子时 vs. 晚子时)
The Chinese double-hour Zi (子时) spans from 23:00 to 01:00:
- **Late Zi Hour (晚子时 / 夜子时)**: 23:00 – 24:00 (before midnight).
- **Early Zi Hour (早子时 / 子正换日)**: 00:00 – 01:00 (after midnight).

There are two major historical traditions for handling births between 23:00 and 24:00:

| Tradition | Day Stem Boundary | Hour Stem Derivation | Philosophical Argument |
|---|---|---|---|
| **Sect 1 (子正换日)** | Midnight (00:00) | Uses tomorrow's stem-branch | Day changes with calendar midnight; hour belongs to the new cycle. |
| **Sect 2 (子初换日 - EastAlmanac Default)** | **23:00 (Start of Zi)** | Uses tomorrow's stem-branch | Zi hour is an indivisible 2-hour unit; when Zi begins, the energetic day begins. |

**EastAlmanac Default**: We implement **Sect 2 (子初换日)** as standard. In traditional cosmology, the Yang energy re-emerges at 23:00 (*一阳初生*). Dividing the Zi hour in half creates internal metaphysical discordance between the earthly branch and the day's energetic pulse.

---

## 3. Structural Attributes Derived for Each Pillar

Every calculated pillar produces comprehensive structural metadata:
1. **Heavenly Stem & Earthly Branch**: Canonical characters, elements, and Yin/Yang polarity.
2. **Hidden Stems (支藏干)**: Each branch houses 1 to 3 hidden stems, categorized by hierarchy:
   - **Main Qi (本气)**: The core element of the branch (e.g., 巳 contains 丙 Fire).
   - **Middle Qi (中气)**: Secondary elemental storage (e.g., 巳 contains 庚 Metal).
   - **Residual Qi (余气)**: Residual trace of the previous phase (e.g., 巳 contains 戊 Earth).
3. **Ten Gods (十神)**: Defined by the relationship between the Day Master (the self) and other stems:
   - Same element: Friend (比肩) / Rob Wealth (劫财)
   - I generate: Eating God (食神) / Hurting Officer (伤官)
   - I control: Direct Wealth (正财) / Indirect Wealth (偏财)
   - Controls me: Direct Officer (正官) / Seven Killings (七杀)
   - Generates me: Direct Seal (正印) / Indirect Seal (偏印)
4. **12 Life Stages / Terrains (十二长生 / 星运)**: The energetic vitality stage of the stem relative to the branch (Birth 长生, Bath 沐浴, Crown 冠带, Officer 临官, Peak 帝旺, Decline 衰, Sickness 病, Death 死, Grave 墓, Extinction 绝, Fetus 胎, Nourish 养).
5. **Nayin (纳音五行)**: The 30 paired elemental sounds assigned to the 60 ganzhi combinations (e.g., 己巳 = 大林木 Great Forest Wood).
6. **Auxiliary Astrological Signs**:
   - **Fetal Origin (胎元)**: Month stem + 1, Month branch + 3.
   - **Fetal Breath (胎息)**: Stem combining with Day stem, Branch combining with Day branch.
   - **Own Sign / Destiny Palace (命宫)** & **Body Sign (身宫)**: Calculated from the relative positions of the sun and birth hour.

---

## 4. Decade Fortunes (大运): Direction and Start Age

Decade fortunes govern ten-year chapters of life. Their derivation follows strict deterministic astronomical rules:

### A. Sequence Direction (顺推 vs. 逆推)
- **Forward (顺行)**: The pillars progress in chronological order along the 60-cycle table.
  - Applied to: **Yang Males** (Year stem is Jia, Bing, Wu, Geng, or Ren) and **Yin Females** (Year stem is Yi, Ding, Ji, Xin, or Gui).
- **Reverse (逆行)**: The pillars regress backwards along the 60-cycle table.
  - Applied to: **Yin Males** and **Yang Females**.

### B. Start Age Calculation (起运岁数)
The moment when the first decade begins is determined by the distance between the birth time and the nearest solar term:
- **Forward Charts**: Distance measured forward to the **next** upcoming solar term (节).
- **Reverse Charts**: Distance measured backward to the **preceding** solar term (节).

**Classical Scale of Equivalence**:
- 3 days $= 1$ full year of life
- 1 day (24 hours) $= 4$ months
- 1 hour $= 5$ days
- 12 minutes $= 1$ day

The engine computes this down to the exact day and month of transition.

---

## 5. Worked Golden Example

- **Input**: Male, born `1990-01-15 14:30:00` (Local wall-clock).
- **Year Pillar**: `己巳` (Earth-Snake, Yin)
  - Because the subject is Male and the year stem 己 is Yin, the chart sequence is **Reverse (逆行)**.
- **Month Pillar**: `丁丑` (Fire-Ox). Born during the solar term Xiaohan (小寒).
- **Day Pillar**: `庚辰` (Metal-Dragon). **Day Master = 庚 (Yang Metal)**.
- **Hour Pillar**: `癸未` (Water-Goat).

### Decade Fortune Progression
- **Start Age**: 4 years old (Calculated transition moment: roughly 1993).
- **Progression (Reverse from Month 丁丑)**:
  1. Age 4–13 (1993–2003): **丙子** (Bing Zi) — Stem: Seven Killings (七杀); Branch: 癸 Water (Hurting Officer).
  2. Age 14–23 (2003–2013): **乙亥** (Yi Hai) — Stem: Direct Wealth (正财); Branch: 壬 Water / 甲 Wood.
  3. Age 24–33 (2013–2023): **甲戌** (Jia Xu) — Stem: Indirect Wealth (偏财); Branch: 戊 Earth / 辛 Metal / 丁 Fire.
  4. Age 34–43 (2023–2033): **癸酉** (Gui You) — Stem: Hurting Officer (伤官); Branch: 辛 Metal (Rob Wealth).
  5. Age 44–53 (2033–2043): **壬申** (Ren Shen) — Stem: Eating God (食神); Branch: 庚 Metal / 壬 Water / 戊 Earth.
  6. Age 54–63 (2043–2053): **辛未** (Xin Wei) — Stem: Rob Wealth (劫财); Branch: 己 Earth / 丁 Fire / 乙 Wood.

---

## Try It Online
Generate and audit your complete Four Pillars chart, hidden stems, and decade transitions:
- **Interactive BaZi Chart Tool**: [https://eastalmanac.com/tools/chart/](https://eastalmanac.com/tools/chart/)
