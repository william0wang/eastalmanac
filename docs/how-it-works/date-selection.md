# Date Selection: The Almanac, Reversed — Additive Weights over 宜忌, Duty Officers, and the Yellow Path

_Last verified: 2026-10_

## TL;DR
The almanac pages answer "what is this day good for"; the date-selection engine answers the reverse — **"which days in my window are good for MY event."** It is a pure client-side scan over the same almanac data the daily pages render: every date in the window is scored by an **additive weight model** over three classical signals — 宜/忌 term matches, the 建除十二神 day officer, and the 黄黑道 twelve stars — plus a personal clash flag when the day's 六冲 animal hits the querent's own zodiac. Six modern events are mapped into the traditional vocabulary; the full mapping and every weight are public.

---

## 1. Events and Their Traditional Mapping

| Event | Primary 宜 terms | Secondary 宜 terms | Favorable duty | Unfavorable duty |
|---|---|---|---|---|
| wedding 结婚 | 嫁娶 | 订盟 纳采 订婚 安床 会亲友 祭祀 祈福 | 成 满 定 开 | 破 危 闭 除 |
| moving 搬家 | 移徙 入宅 | 安床 安香 出火 修造 会亲友 | 成 满 开 定 | 破 危 闭 执 |
| business-opening 开业 | 开市 | 挂匾 交易 立券 纳财 求财 开光 祭祀 | 开 成 满 | 破 危 闭 执 |
| contract-signing 签约 | 立券 交易 订盟 | 纳财 会亲友 会友 | 定 成 建 | 破 危 闭 |
| travel 出行 | 出行 | 乘船 渡水 会友 会亲友 | 建 成 开 | 破 危 闭 除 |
| job-interview 求职 | 赴任 见贵 | 会友 会亲友 出行 | 建 开 成 | 破 危 闭 |

Duty grading follows the 建除十二神 lore (e.g. 执 disfavors moving and openings; 除 disfavors weddings and long journeys).

## 2. The Additive Weight Model

| Signal | Weight |
|---|---|
| Primary 宜 term matches | **+3** each |
| Secondary 宜 term matches | +1 each |
| Primary term appears in the day's 忌 | **−4** |
| Secondary term in 忌 | −1 |
| Duty officer favorable for the event | +2 |
| Duty officer unfavorable | −3 |
| Yellow-path star (青龙 明堂 金匮 天德 玉堂 司命) | +1 |
| Black-path star (天刑 朱雀 白虎 天牢 玄武 勾陈) | −1 |
| Day clashes the querent's own zodiac (六冲) | **−5** |

The day's net score maps to grades: **best ≥ 5 · good ≥ 3 · fair ≥ 1 · else avoid**. Thresholds were calibrated over a full 2026 sweep so every event reaches "best" days in most months. The page layer shows the reasons, never a composite percentage — same no-false-precision principle as synastry.

## 3. The Personal Clash Flag

Each day branch clashes (六冲) the branch six steps away — 寅日冲猴, 子日冲马. Given a birth year, the querent's zodiac follows the **立春** sixty-cycle convention (same as the annual-fortune engine — not the lunar-new-year split chengu uses). A clash both subtracts 5 and typically flips the grade (see §5).

## 4. The Window Scan

Every day in the inclusive window is evaluated (`from`/`to`, hard cap **400 days**); days graded *avoid* are dropped; the rest rank by score (descending), ties by earlier date; default 10 results, cap 60. Window arithmetic uses pure epoch-day math (Hinnant civil-from-days) — no `Date` objects, identical across builds.

## 5. Worked Golden Examples (all machine-pinned)

**2026-10-12 己未 — wedding:** 宜嫁娶 (+3), 宜祭祀 (+1), 朱雀 black star (−1) → **score 3, good**. The same day with birthYear 1985 (牛): 己未日冲牛 (−5) → **−2, avoid** — the clash flips the verdict. With 1990 (马): no clash, score untouched at 3.

**2026-10-07 甲寅 执日 — the anti-pick:** wedding: 忌嫁娶 (−4), 忌安床 (−1), 忌祭祀 (−1), 青龙 (+1) → **−5, avoid**. Moving is worse: 忌入宅 (−4), 忌安床 (−1), 执 duty (−3), 青龙 (+1) → **−7, avoid**.

**2026-10-14 辛酉 — the trade-off:** 闭日 (−3) but 宜嫁娶 (+3), 安床 (+1), 祭祀 (+1), 祈福 (+1), 天德 yellow star (+1) → **+4, good** — a weak officer rescued by strong term matches.

**2026-11-26 甲辰 (司命黄道) — wedding → 7, best.**

**1949-10-01 甲子 (平日/司命) — business-opening → 2, fair** (duty 平 is ungraded for openings; only 祭祀 +1 and 司命 +1 fire).

**Three-day window 2026-10-12..14, wedding:** ranks `10-13 (7, best)` → `10-14 (4, good)` → `10-12 (3, good)`.

## 6. Full-Year Invariants (2026 sweep, machine-checked)

- The score is **exactly** the sum of reason weights; the grade matches the thresholds — verified for every day × every event.
- 2026 grade counts pin the calibration, e.g. wedding `83 best / 43 good / 52 fair / 187 avoid`, job-interview `4 / 46 / 118 / 197` (its classical terms 赴任/见贵 are rare — 见贵 never appears in 2026 recommends — so 5 is its realistic ceiling).
- tyme4ts never lists the same term in both 宜 and 忌 on any day (the matcher's core assumption).
- Identical output when the window is re-scanned; results equal independent day-by-day stepping (verified across a leap-February window).

---

## Try It Online
- **Date Selection Tool**: [https://eastalmanac.com/tools/dates/](https://eastalmanac.com/tools/dates/)
