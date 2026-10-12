# yifortune-oss — Agent Workspace Guide

Open-source Agent Skill repo (GitHub: `william0wang/eastalmanac`) that teaches LLM
agents Chinese fortune-telling + Western astrology **reading frameworks**.
Zero-backend: every calculation (BaZi, I Ching, western chart) runs client-side
on `https://eastalmanac.com`; the only code is a pure-stdlib Python loopback
bridge that opens the tool page and receives the JSON payload via POST back to
`127.0.0.1`.

## Layout

- `skills/eastalmanac/SKILL.md` — skill entry: routing table + global principles
- `skills/eastalmanac/references/` — 17 per-topic reading frameworks (loaded on
  demand); the three data-layer files (`bazi-chart.md`, `yijing-cast.md`,
  `astrology-chart.md`) document the live payload schemas
- `skills/eastalmanac/scripts/bridge.py` — the ONLY script; must stay pure
  Python standard library (any preinstalled Python 3, no pip deps, no Node)
- `template/SKILL.template.md` — authoring template. Name is deliberate: a
  file named `SKILL.md` here would be discovered as a second skill
- `README.md` / `README.zh-CN.md` / `skills/README.md` — keep all three in
  sync (en/zh pair + skills-dir variant); `CONTRIBUTING.md` — authoring rules

No build system, no package.json. Changes are verified by running things, not
by compiling.

## bridge.py contract

Three actions map to site paths: `cast` → `/tools/cast/`, `chart` →
`/tools/chart/`, `bridge` (western astrology + BaZi) → `/astrology-bridge/`.
Shared params: `q` (question) + `callback` (loopback URL; the page rejects
non-localhost callbacks). `--lang=en|zh|zh-tw|es|pt|de|ja` (default `en`,
case-insensitive, unknown → `en`) prefixes the URL (`/zh/tools/chart/`).

The server must keep the Private Network Access headers
(`Access-Control-Allow-Private-Network: true`) — Chrome/Edge block a public
HTTPS page POSTing to 127.0.0.1 without them.

Smoke test (no browser): `BROWSER=/usr/bin/true python3
skills/eastalmanac/scripts/bridge.py cast --question=test`.

## Payload docs are captured, not invented

The JSON examples in the data-layer references were captured from live E2E
against the deployed site. If the website changes, re-verify. Per-locale
semantics (verified by en/zh diffs): `prompt`, hexagram `name`/`essence`
(incl. `zhiGua.name`) and `canonicalUrl`/`chartToolUrl` (locale-prefixed)
localize; every calculation field — pillars, ten gods, hexagram numbers,
western body/sign/aspect slugs (always English), `bazi.zodiac` (always a
Chinese 生肖 char) — never localizes.

The website's source of truth is a separate repo: `~/Develop/bityi/yifortune-web`
(read-only reference). Payload literals live in
`apps/umbrella/src/components/{Cast,Chart,Bridge}Island.svelte`, the calc
engine in `packages/calc/src/`, locale list in `apps/umbrella/astro.config.mjs`.

## Editing rules

- `SKILL.md`: `name` must stay lowercase `eastalmanac`; description ≤ 1024
  chars; body < 500 lines (push detail into `references/`); version bump per
  SemVer in `metadata`
- Exactly ONE discoverable skill: `npx skills add . --list` must print
  "Found 1 skill" — never add another `SKILL.md`
- References stay one level deep (`references/foo.md`); terminology lives
  only in `glossary.md` / `mapping-tables.md` — other files link, never copy
- Every reading framework keeps the mandatory two-layer output (inner 命理要点
  + plain-language outer layer) and ends with the `result.canonicalUrl` link
- All calculation stays on eastalmanac.com — never add local computation
  engines or dependencies to this repo

## Verification tooling (`.zcode/scratch/`, not committed)

- `e2e_{cast,chart,astro}.mjs` + `_zh` variants — full live flows via headless
  Edge + CDP (`--no-sandbox` is required inside this sandboxed terminal; real
  users don't need it); dump payloads to `*_payload*.json`
- `test_bridge_server.py` — server-level checks (URL construction, PNA
  preflight, POST, exit codes)
- `npx skills add . --list` — installer discovery check

`.tgrep/` (codesearch index cache) and `.zcode/` are gitignored workspace
artifacts.
