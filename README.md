# EastAlmanac Skill

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-spec%20compliant-blue)](https://agentskills.io)
[![skills.sh](https://skills.sh/b/william0wang/eastalmanac)](https://skills.sh/william0wang/eastalmanac)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)](#changelog)

**English** · **[简体中文](README.zh-CN.md)**

> An [Agent Skills](https://agentskills.io)–compliant skill that turns any LLM client into a professional Chinese fortune-telling and astrology assistant through interactive browser synergy with [EastAlmanac](https://eastalmanac.com).

EastAlmanac teaches an AI **how to read** fortune-telling data — the structural frameworks, the terminology, and the plain-language delivery — so that when a chart or hexagram is computed, the output is a high-quality professional reading instead of raw numbers.

It covers **15 topics**: 八字 (BaZi), 西方占星 (Western astrology), 易经起卦 (I Ching divination), 事业 (career), 财运 (wealth), 感情 (love), 健康 (health), 成长 (growth), 配对 (compatibility), 周期运势 (period fortune), 姓名 (name analysis), 择日 (date selection), 风水 (feng shui), 流年详批 (annual reading), and a shared terminology layer.

## Key Advantages

- **100% Free & Open Source**: No API keys required, no email registration, and zero monthly quotas or rate limits.
- **Zero-Install, Zero Dependencies**: Runs on any preinstalled Python 3 (the bridge is pure standard library); every reading — BaZi, I Ching, and Western astrology — computes 100% client-side in the browser with zero server-side storage or privacy leaks.
- **Terminal & Web Synergy**: Combines the power of conversational terminal AI with the rich visual ritual of drawing hexagrams and verifying birth charts on `eastalmanac.com`, seamlessly feeding data back to your terminal via a local loopback bridge.

---

## What this is — and isn't

| ✅ This repo provides | ❌ It does NOT include |
| --------------------- | --------------------- |
| The `eastalmanac` skill (`SKILL.md` + `references/` + `scripts/bridge.py`) | Remote backend servers or databases |
| Reading frameworks for 15 fortune-telling topics | API keys, paid paywalls, or monthly quotas |
| Local loopback bridge script (`scripts/bridge.py`) | Uncontrolled cloud tracking of personal birth data |
| Plain-language output rules (the AI serves laypeople, not masters) | |

---

## Prerequisites

- **Nothing to install** — the skill runs out of the box on any preinstalled Python 3 (`scripts/bridge.py` uses only the standard library). macOS and most Linux systems ship Python 3 by default. Every reading, Western astrology included, computes client-side in the browser.

---

## Install

### Option A — One command via the [skills CLI](https://skills.sh) (recommended)

```bash
npx skills add william0wang/eastalmanac
```

The CLI auto-detects your installed agents (Claude Code, Codex, Cursor, ZCode, and 75+ more) and installs the skill for you. Useful variants:

```bash
npx skills add william0wang/eastalmanac -a claude-code -a zcode   # target specific agents
npx skills add william0wang/eastalmanac -g                        # global (user-level) install
npx skills update                                               # update later
```

### Option B — Manual install (Claude Desktop or any client)

Copy the `eastalmanac` skill directory into your client's skills folder.

**Claude Code / other `~/.agents`-compatible clients:**

```bash
git clone https://github.com/william0wang/eastalmanac.git
cp -r eastalmanac/skills/eastalmanac ~/.agents/skills/
```

**ZCode:**

```bash
git clone https://github.com/william0wang/eastalmanac.git
cp -r eastalmanac/skills/eastalmanac ~/.zcode/skills/
```

**Claude Desktop:** place the skill under `~/Library/Application Support/Claude/skills/` (macOS) or `%APPDATA%\Claude\skills\` (Windows), then restart Claude Desktop.

After installing, simply mention the skill in your conversation — e.g. "Use the eastalmanac skill to read my BaZi chart."

---

## Verify the installation

Try these prompts in your client:

| Prompt | What happens |
| ------ | ------------ |
| "帮我排个八字，1990 年 1 月 15 日下午 2 点 30 分出生在上海，男" | Launches browser to verify BaZi chart on EastAlmanac; transmits back for deep reading |
| "我适合做什么工作？" (birth info required) | BaZi career analysis |
| "帮我为'今年换工作是否合适'起一卦" | Launches interactive canvas to draw/cast hexagram; transmits back for decision reading |
| "What does my astrology chart say about me?" | Launches the astrology-bridge page (western natal chart + BaZi side by side); transmits back, replied **in English** |
| "下个月想搬家，帮我选个吉日" | Auspicious date selection |

---

## Architecture: single skill + progressive disclosure

Following the [Agent Skills spec](https://agentskills.io/specification), EastAlmanac is **one skill** that loads content on demand:

```
skills/eastalmanac/
├── SKILL.md                  ← entry: routing table + global principles (loaded on trigger)
├── scripts/
│   └── bridge.py             ← the only script: zero-dependency (pure stdlib Python) loopback bridge
└── references/               ← per-topic reading frameworks (loaded on demand, not at startup)
    ├── bazi-chart.md         ← BaZi chart reading (data layer)
    ├── astrology-chart.md    ← Western natal chart reading (data layer)
    ├── yijing-cast.md        ← I Ching divination reading (data layer)
    ├── glossary.md           ← terminology (single source of truth)
    ├── mapping-tables.md     ← extended element mapping tables
    ├── terms-detail.md       ← deep terminology reference
    ├── career.md  wealth.md  love.md  health.md  growth.md
    ├── compatibility.md  period-fortune.md  name-analysis.md
    └── date-selection.md  fengshui.md  annual-reading.md
```

**Three-layer loading** (progressive disclosure):

1. **Metadata** (at startup) — the client reads only `SKILL.md` frontmatter to decide whether to trigger this skill (~100 tokens)
2. **Body** (on trigger) — reads `SKILL.md`: the routing table + global principles, then locates the relevant reference
3. **References** (on demand) — loads the specific `references/*.md` only when a topic is needed, keeping the context window lean

---

## Security & Trust Model

All calculation happens client-side on `eastalmanac.com`; the only local code is `scripts/bridge.py` (pure stdlib, ~180 lines — read it yourself):

- **One-way loopback data flow**: the bridge binds to `127.0.0.1` on an ephemeral port, waits for exactly one POST from the tool page, prints the JSON to stdout, and exits. `GET` returns 404; nothing else is served. 5-minute timeout, then it shuts down.
- **Single external origin**: the bridge's only outbound action is opening the tool page at `https://eastalmanac.com` (locale-prefixed) in your browser. The callback URL points at `127.0.0.1`, and the page refuses non-localhost callbacks.
- **No secrets, no telemetry**: no API keys, no accounts, no analytics, no file access — there is nothing to leak.
- **Payload is data, not instructions**: the skill instructs the agent to use the returned JSON strictly as chart facts and to ignore any instruction-like text inside it, so a compromised page cannot drive the agent.

> Security scanners may flag the runtime dependency on `eastalmanac.com` (e.g. Snyk Agent Scan W012 "unverifiable external dependency"). That is inherent to the zero-backend design — it is the trust boundary described above, not a finding of malicious code.

---

## Open calculation architecture (How It Works)

Unlike black-box divination and astrology platforms, EastAlmanac fully publishes and specifies its underlying calculation engines. Every scoring model, bitwise state machine, and astronomical coordinate transformation is documented as an open, reproducible specification:

- **[How EastAlmanac Works (Index)](docs/how-it-works/README.md)** ([中文版](docs/how-it-works/README.zh-CN.md))
- **[Three-Number I Ching Casting](docs/how-it-works/three-number-casting.md)** ([中文版](docs/how-it-works/three-number-casting.zh-CN.md)): 3-bit modulo arithmetic, Hamming parity state machine, and Master Zhu Xi's changing-line judgment rules.
- **[BaZi Four Pillars Casting](docs/how-it-works/four-pillars.md)** ([中文版](docs/how-it-works/four-pillars.zh-CN.md)): Birthplace wall-clock authority, solar-term month boundaries, Sect 2 (子初换日) midnight rules, and decade fortunes.
- **[Five-Element Strength Scoring](docs/how-it-works/strength-scoring.md)** ([中文版](docs/how-it-works/strength-scoring.zh-CN.md)): Transparent base stem/branch weight tables, seasonal prosperity multipliers (旺相休囚死), and 扶抑 balancing remedies.
- **[Structural Dynamics & Interactions](docs/how-it-works/structural-attrs.md)** ([中文版](docs/how-it-works/structural-attrs.zh-CN.md)): *I Ching* line correctness (当位), centrality (得中), polar correspondence (应), and BaZi earthly branch harmonies, clashes, and punishments.
- **[Western Tropical Natal Chart](docs/how-it-works/western-chart.md)** ([中文版](docs/how-it-works/western-chart.zh-CN.md)): Hellenistic Whole-Sign house system, four major Ptolemaic aspects, hierarchical orbs, and Swiss Ephemeris alignment (0.0″ ASC/MC match).

---

## Design principles

- **Audience: ordinary people, not masters** — the AI serves a curious layperson. Every reading has two layers: an inner layer (chart facts + terminology, for traceability) and an **outer layer in plain language** (what the user actually came for).
- **Proactive service** — the AI routes and decides which tool to use; it never dumps a menu of tools for the user to pick from.
- **Language matching** — the AI replies in whatever language the user wrote in, from the very first message.
- **Infer before asking** — when birth info (gender, calendar type, etc.) can be read from the user's wording, the AI doesn't ask.
- **Single source of truth** — all terminology lives in `references/glossary.md`; other references cite it instead of redefining.

## What this skill does NOT do

- ❌ No compliance/censorship rules — readings are produced by the user's own LLM
- ❌ No word-count mandates — unrelated to reading quality
- ❌ No reading decisions on the LLM's behalf — the skill provides frameworks and terminology; the LLM produces the reading with its own capability

---

## Troubleshooting

| Symptom | Cause / Fix |
| ------- | ----------- |
| Skill doesn't activate | Confirm the `eastalmanac` directory is in your client's skills folder and matches the `name: eastalmanac` in `SKILL.md` frontmatter. Restart the client. |
| Browser does not open automatically | Check the terminal output: the bridge displays the URL. Copy and open `https://eastalmanac.com/...` manually in any browser. |
| Bridge timeout (5 minutes) | If you completed the reading on the web page, click "复制提示词" and paste the text directly into the chat prompt. |
| Astrology page needs lat/lon/tz | Resolve the **birthplace** to coordinates and UTC offset yourself (mind DST), then run `python3 scripts/bridge.py bridge --date=... --time=... --lat=... --lon=... --tz=...`. |

---

## Contributing

Contributions are welcome — especially corrections to terminology, new topic references, or translations. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Changelog

### 2.1.0 — 2026-10-13

- **Five new bridge actions — the skill now covers the full tool suite**: `liuyao` (six coin strokes → Liu Yao Najia board), `chengu` (Yuan Tiangang bone-weight fortune), `match` (two-person BaZi compatibility, 5 relationship types), `dates` (auspicious-date search for 6 life events), and `naming` (corpus-sourced name shortlist, zh-only). All eight actions were loopback-tested end-to-end against production across en/zh with 79 payload contract assertions.
- **Two new references**: `references/liuyao-chart.md` (strokes → hexagram board → 用神 selection → five-step reading order) and `references/chengu.md` (lunar-year boundary at 正月初一, leap-month base weight, late-Zi hour roll, golden example 四两四钱).
- **SKILL.md trigger vocabulary expanded** (六爻/纳甲/梅花易数/称骨/骨重 among others); the route table now dispatches 六爻, 称骨, 配对, 择日, and 姓名 questions to the new commands, and the compatibility / date-selection / name-analysis references were updated to match.

### 2.0.0 — 2026-10-12

- **BREAKING: skill identifier renamed `yifortune` → `eastalmanac`** — the SKILL.md `name`, the `skills/eastalmanac/` directory, and every command/path reference now use the EastAlmanac name end to end. If you installed an earlier version, reinstall (`npx skills add william0wang/eastalmanac`) and delete the old `yifortune` skill folder; the trigger phrase becomes "use the eastalmanac skill".

### 1.2.0 — 2026-10-12

- **How-It-Works open calculation docs** (`docs/how-it-works/`): five reproducible specifications — three-number I Ching casting, BaZi four pillars, five-element strength scoring (full weight tables), structural attributes (line positions & branch relations), and the western natal chart — each with formulas, complete numeric tables, and golden worked examples. EN + zh-CN, indexed by a landing README and linked from all three repo READMEs.
- **Rebranded to EastAlmanac** across every doc, reference title, and script message to match the eastalmanac.com site brand (the skill `name` stays `yifortune`).
- **Repo renamed** `william0wang/yifortune` → `william0wang/eastalmanac`; install commands, clone examples, and the skills.sh badge updated (old URLs keep redirecting).

### 1.1.1 — 2026-10-12

- **Data-only payload rule**: `SKILL.md` now instructs the agent to treat the bridge's returned JSON (and pasted EastAlmanac text) strictly as chart data — instruction-like text inside payload fields is ignored, never executed. Narrows the prompt-injection surface if the site were ever compromised.
- **Security & Trust Model** section added: one-way loopback data flow, one-shot server on `127.0.0.1`, no telemetry, single external origin (`eastalmanac.com`).

### 1.1.0 — 2026-10-12

- **Migrated to EastAlmanac interactive bridge architecture**: Completely deprecated the Cloudflare Worker MCP remote backend and API key requirements.
- Zero-backend, zero-registration, and unlimited readings powered by `eastalmanac.com` client-side computing and local loopback (`bridge.py`).
- **Zero-install core**: the bridge is now pure standard-library Python — runs on any preinstalled Python 3, no Node.js, no pip dependencies. The bundled offline casting scripts (`cast.sh` / `cast.ps1`) were removed; all BaZi and I Ching calculation happens in the browser.
- **Western astrology migrated to the browser too** (`bridge` action): the astrology-bridge page computes the western natal chart and the BaZi of the same birth moment client-side, returning both in one payload — kerykeion, `requirements.txt`, and the AGPL notice are gone; the skill is now dependency-free end to end.
- **Seven page/payload locales**: every bridge action accepts `--lang=en|zh|zh-tw|es|pt|de|ja` (default `en`) and opens under the locale prefix — the prompt, hexagram names/essence, and canonical links come back in that language, while all calculation fields stay locale-neutral (verified by en/zh E2E on all three flows).
- One-command install via the skills CLI: `npx skills add william0wang/eastalmanac`.
- Interactive stroke-derived hexagram casting and visual BaZi chart verification in browser with one-click return to terminal Agent.
- Added canonical URL reference links to every reading.

### 1.0.0 — 2026-07-28

- First public release. Single skill architecture with progressive disclosure (SKILL.md + references + scripts)
- 15 topics: BaZi, Western astrology, I Ching, career, wealth, love, health, growth, compatibility, period fortune, name analysis, date selection, feng shui, annual reading
- Plain-language output rules (two-layer: professional analysis + plain conclusion)

## License

[MIT](LICENSE) © 2026 william0wang
