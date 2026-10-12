# YiFortune Skill

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-spec%20compliant-blue)](https://agentskills.io)
[![skills.sh](https://skills.sh/b/william0wang/yifortune)](https://skills.sh/william0wang/yifortune)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.1.0-green.svg)](#changelog)

**English** · **[简体中文](README.zh-CN.md)**

> An [Agent Skills](https://agentskills.io)–compliant skill that turns any LLM client into a professional Chinese fortune-telling and astrology assistant through interactive browser synergy with [EastAlmanac](https://eastalmanac.com).

YiFortune teaches an AI **how to read** fortune-telling data — the structural frameworks, the terminology, and the plain-language delivery — so that when a chart or hexagram is computed, the output is a high-quality professional reading instead of raw numbers.

It covers **15 topics**: 八字 (BaZi), 西方占星 (Western astrology), 易经起卦 (I Ching divination), 事业 (career), 财运 (wealth), 感情 (love), 健康 (health), 成长 (growth), 配对 (compatibility), 周期运势 (period fortune), 姓名 (name analysis), 择日 (date selection), 风水 (feng shui), 流年详批 (annual reading), and a shared terminology layer.

## Key Advantages

- **100% Free & Open Source**: No API keys required, no email registration, and zero monthly quotas or rate limits.
- **Zero-Install, Zero Dependencies**: Runs on any preinstalled Python 3 (the bridge is pure standard library); every reading — BaZi, I Ching, and Western astrology — computes 100% client-side in the browser with zero server-side storage or privacy leaks.
- **Terminal & Web Synergy**: Combines the power of conversational terminal AI with the rich visual ritual of drawing hexagrams and verifying birth charts on `eastalmanac.com`, seamlessly feeding data back to your terminal via a local loopback bridge.

---

## What this is — and isn't

| ✅ This repo provides | ❌ It does NOT include |
| --------------------- | --------------------- |
| The `yifortune` skill (`SKILL.md` + `references/` + `scripts/bridge.py`) | Remote backend servers or databases |
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
npx skills add william0wang/yifortune
```

The CLI auto-detects your installed agents (Claude Code, Codex, Cursor, ZCode, and 75+ more) and installs the skill for you. Useful variants:

```bash
npx skills add william0wang/yifortune -a claude-code -a zcode   # target specific agents
npx skills add william0wang/yifortune -g                        # global (user-level) install
npx skills update                                               # update later
```

### Option B — Manual install (Claude Desktop or any client)

Copy the `yifortune` skill directory into your client's skills folder.

**Claude Code / other `~/.agents`-compatible clients:**

```bash
git clone https://github.com/william0wang/yifortune.git
cp -r yifortune/skills/yifortune ~/.agents/skills/
```

**ZCode:**

```bash
git clone https://github.com/william0wang/yifortune.git
cp -r yifortune/skills/yifortune ~/.zcode/skills/
```

**Claude Desktop:** place the skill under `~/Library/Application Support/Claude/skills/` (macOS) or `%APPDATA%\Claude\skills\` (Windows), then restart Claude Desktop.

After installing, simply mention the skill in your conversation — e.g. "Use the yifortune skill to read my BaZi chart."

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

Following the [Agent Skills spec](https://agentskills.io/specification), YiFortune is **one skill** that loads content on demand:

```
skills/yifortune/
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
| Skill doesn't activate | Confirm the `yifortune` directory is in your client's skills folder and matches the `name: yifortune` in `SKILL.md` frontmatter. Restart the client. |
| Browser does not open automatically | Check the terminal output: the bridge displays the URL. Copy and open `https://eastalmanac.com/...` manually in any browser. |
| Bridge timeout (5 minutes) | If you completed the reading on the web page, click "复制提示词" and paste the text directly into the chat prompt. |
| Astrology page needs lat/lon/tz | Resolve the **birthplace** to coordinates and UTC offset yourself (mind DST), then run `python3 scripts/bridge.py bridge --date=... --time=... --lat=... --lon=... --tz=...`. |

---

## Contributing

Contributions are welcome — especially corrections to terminology, new topic references, or translations. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Changelog

### 1.1.0 — 2026-10-12

- **Migrated to EastAlmanac interactive bridge architecture**: Completely deprecated the Cloudflare Worker MCP remote backend and API key requirements.
- Zero-backend, zero-registration, and unlimited readings powered by `eastalmanac.com` client-side computing and local loopback (`bridge.py`).
- **Zero-install core**: the bridge is now pure standard-library Python — runs on any preinstalled Python 3, no Node.js, no pip dependencies. The bundled offline casting scripts (`cast.sh` / `cast.ps1`) were removed; all BaZi and I Ching calculation happens in the browser.
- **Western astrology migrated to the browser too** (`bridge` action): the astrology-bridge page computes the western natal chart and the BaZi of the same birth moment client-side, returning both in one payload — kerykeion, `requirements.txt`, and the AGPL notice are gone; the skill is now dependency-free end to end.
- **Seven page/payload locales**: every bridge action accepts `--lang=en|zh|zh-tw|es|pt|de|ja` (default `en`) and opens under the locale prefix — the prompt, hexagram names/essence, and canonical links come back in that language, while all calculation fields stay locale-neutral (verified by en/zh E2E on all three flows).
- One-command install via the skills CLI: `npx skills add william0wang/yifortune`.
- Interactive stroke-derived hexagram casting and visual BaZi chart verification in browser with one-click return to terminal Agent.
- Added canonical URL reference links to every reading.

### 1.0.0 — 2026-07-28

- First public release. Single skill architecture with progressive disclosure (SKILL.md + references + scripts)
- 15 topics: BaZi, Western astrology, I Ching, career, wealth, love, health, growth, compatibility, period fortune, name analysis, date selection, feng shui, annual reading
- Plain-language output rules (two-layer: professional analysis + plain conclusion)

## License

[MIT](LICENSE) © 2026 william0wang
