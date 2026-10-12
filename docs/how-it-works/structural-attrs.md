# Structural Dynamics: I Ching Line Positions and BaZi Earthly Branch Interactions

_Last verified: 2026-10_

## TL;DR
Beyond raw hexagram names and five-element point tallies lies the structural grammar of Chinese metaphysics: why is a specific line in the *I Ching* auspicious, and why does an earthly branch in BaZi create turbulence? EastAlmanac evaluates these using a formal relational engine. For the *I Ching*, every line is audited for **Correctness (当位)**, **Centrality (得中)**, **Polar Correspondence (应)**, and **Adjacency Dynamics (乘/承/比)** alongside the interior **Nuclear Hexagram (互卦)**. For BaZi, every branch pair is tested for **Three Harmonies (三合)**, **Six Combinations (六合)**, **Six Clashes (六冲)**, **Three Punishments (三刑)**, and **Six Harms (六害)**.

---

## 1. I Ching Structural Grammar

An *I Ching* hexagram is not a static glyph; it is a layered vertical energetic field spanning from earth (Line 1) to heaven (Line 6).

### A. Line Placement: Correctness (当位) and Centrality (得中)

Each of the six line positions carries an innate Yin or Yang character:
- **Yang Positions (阳位)**: Odd positions — Line 1 (初爻), Line 3 (三爻), Line 5 (五爻).
- **Yin Positions (阴位)**: Even positions — Line 2 (二爻), Line 4 (四爻), Line 6 (上爻).

| Positional Property | Definition & Rule | Metaphysical Significance |
|---|---|---|
| **Correct (当位 / 得位)** | A Yang line (—) occupies an odd position, OR a Yin line ($--$) occupies an even position. | Action aligns with rank; behavior suits the environmental context. |
| **Incorrect (不当位 / 失位)** | A Yang line occupies an even position, OR a Yin line occupies an odd position. | Friction between innate character and circumstantial responsibility. |
| **Central (得中)** | Line 2 (center of the inner trigram) OR Line 5 (center of the outer trigram). | Moderation, balance, and freedom from partisan extremes. |
| **Central and Correct (中正)** | **Line 2 is Yin ($--$)** OR **Line 5 is Yang (—)**. | The supreme ideal in *I Ching* philosophy: virtue harmonized with authority. |

---

### B. Relational Dynamics: Correspondence (应) and Adjacency (比, 乘, 承)

Lines do not exist in isolation; they interact across distance and proximity:

#### 1. Polar Correspondence (应 / 正应)
The hexagram pairs inner and outer trigram counterparts:
- **Pair 1**: Line 1 (初爻) $\longleftrightarrow$ Line 4 (四爻)
- **Pair 2**: Line 2 (二爻) $\longleftrightarrow$ Line 5 (五爻) — *The Prime Minister & Sovereign Pair*
- **Pair 3**: Line 3 (三爻) $\longleftrightarrow$ Line 6 (上爻)

**Rule of Response**:
- **Responding (有应 / 正应)**: One line is Yin and the other is Yang. Opposite polarities attract, establishing resonance and support across realms.
- **Hostile / Non-Responding (敌应 / 无应)**: Both lines share identical polarity (Yang-Yang or Yin-Yin). They repel each other, indicating lack of external assistance.

#### 2. Immediate Adjacency (比, 乘, 承)
When lines are direct physical neighbors (at positions `lineIndex` and `lineIndex + 1`):
- **Bearing / Supporting (承)**: A lower line supporting an upper line.
  - *Classically auspicious*: **Yin supports Yang (阴承阳)** — Receptivity humbly bearing strength from below.
- **Riding / Overstepping (乘)**: An upper line standing atop a lower line.
  - *Classically adverse*: **Yin rides Yang (阴乘阳)** — Weakness usurping power over strength from above (often linked to insubordination or precarious burden).

---

### C. The Nuclear Hexagram (互卦): The Hidden Interior Momentum
While the primary hexagram shows outer circumstances, the **Nuclear Hexagram (互卦)** reveals the core internal dynamic:
- **Lower Nuclear Trigram**: Formed by Lines 2, 3, and 4.
- **Upper Nuclear Trigram**: Formed by Lines 3, 4, and 5.
- The two overlapping 3-line clusters generate a brand new 6-line hexagram that exposes hidden developmental trajectories within the primary situation.

---

## 2. BaZi Earthly Branch Relational System

The 12 Earthly Branches (子, 丑, 寅, 卯, 辰, 巳, 午, 未, 申, 酉, 戌, 亥) form geometric energetic circuits on the celestial dial:

### A. Three Harmonies (三合局)
Trines separated by 120° that combine their directional energies into a dominant elemental reservoir:

| Harmonic Group | Earthly Branches Involved | Resulting Element | Cardinal Focus |
|---|---|---|---|
| **Water Frame** | **申 (Monkey) — 子 (Rat) — 辰 (Dragon)** | **Water (水)** | Birth in Shen, Peak in Zi, Tomb in Chen |
| **Wood Frame** | **亥 (Pig) — 卯 (Rabbit) — 未 (Goat)** | **Wood (木)** | Birth in Hai, Peak in Mao, Tomb in Wei |
| **Fire Frame** | **寅 (Tiger) — 午 (Horse) — 戌 (Dog)** | **Fire (火)** | Birth in Yin, Peak in Wu, Tomb in Xu |
| **Metal Frame** | **巳 (Snake) — 酉 (Rooster) — 丑 (Ox)** | **Metal (金)** | Birth in Si, Peak in You, Tomb in Chou |

> **Half-Combinations (半合)**: Any two members meeting in a chart (e.g., 申-子 or 子-辰) form a potent partial harmonic alliance.

---

### B. Six Combinations (六合)
Intimate complementary pairings between adjacent or polar sectors:
- **子 (Rat) + 丑 (Ox)** $\longrightarrow$ Earth (土)
- **寅 (Tiger) + 亥 (Pig)** $\longrightarrow$ Wood (木)
- **卯 (Rabbit) + 戌 (Dog)** $\longrightarrow$ Fire (火)
- **辰 (Dragon) + 酉 (Rooster)** $\longrightarrow$ Metal (金)
- **巳 (Snake) + 申 (Monkey)** $\longrightarrow$ Water (水)
- **午 (Horse) + 未 (Goat)** $\longrightarrow$ Solar/Lunar Earth (土/日月)

---

### C. Six Clashes (六冲)
Direct 180° geometric oppositions on the dial (`(branchIndexA − branchIndexB + 12) mod 12 = 6`):
- **子 (Rat) $\longleftrightarrow$ 午 (Horse)**: Water vs. Fire; emotional volatility and directional upheaval.
- **丑 (Ox) $\longleftrightarrow$ 未 (Goat)**: Damp Earth vs. Dry Earth; structural shifting and career friction.
- **寅 (Tiger) $\longleftrightarrow$ 申 (Monkey)**: Wood vs. Metal; movement, transit, and road events.
- **卯 (Rabbit) $\longleftrightarrow$ 酉 (Rooster)**: Wood vs. Metal; relationship tension and boundary ruptures.
- **辰 (Dragon) $\longleftrightarrow$ 戌 (Dog)**: Earth gate clash; property, foundation, and belief reassessments.
- **巳 (Snake) $\longleftrightarrow$ 亥 (Pig)**: Fire vs. Water; mental restlessness and travel shifts.

---

### D. Three Punishments (三刑)
Complex rotational frictions reflecting internal stress or ethical tests:
1. **Ungrateful Punishment (无恩之刑)**: **寅 (Tiger) $\longrightarrow$ 巳 (Snake) $\longrightarrow$ 申 (Monkey)**. Involves cold pragmatism or broken reciprocal loyalty.
2. **Bullying Punishment (恃势之刑)**: **丑 (Ox) $\longrightarrow$ 戌 (Dog) $\longrightarrow$ 未 (Goat)**. Clashing under excess pride or bureaucratic entanglements.
3. **Uncivilized Punishment (无礼之刑)**: **子 (Rat) $\longleftrightarrow$ 卯 (Rabbit)**. Boundaries breached between generations or intimate partners.
4. **Self-Punishment (自刑)**: **辰-辰, 午-午, 酉-酉, 亥-亥**. When identical branches double up, the element turns inward into obsessive rumination.

---

### E. Six Harms (六害)
Disturbances arising when a third branch clashes with your primary combination partner:
- **子未害**, **丑午害**, **寅巳害**, **卯辰害**, **申亥害**, **酉戌害**.

### Special Coexistence Note: 巳 and 申
When **巳 (Snake)** and **申 (Monkey)** meet in a chart, the engine simultaneously flags both **Six Combinations (六合)** AND **Three Punishments (三刑)**. This coexistence (*合中带刑*, "combination harboring punishment") faithfully mirrors classical Chinese doctrine: alliance and underlying tension cohabiting within the same relationship.

---

## Try It Online
Inspect full line attributes, nuclear hexagrams, and branch clash matrices in real-time:
- **Interactive I Ching Engine**: [https://eastalmanac.com/tools/cast/](https://eastalmanac.com/tools/cast/)
- **Interactive BaZi Chart Tool**: [https://eastalmanac.com/tools/chart/](https://eastalmanac.com/tools/chart/)
