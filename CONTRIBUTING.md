# Contributing to EastAlmanac Skill

Thanks for your interest in improving the EastAlmanac skill! This guide covers the most common contribution types.

## Repository layout

```
skills/eastalmanac/
├── SKILL.md              ← entry: routing table + global principles (edit carefully — affects every reading)
├── references/           ← per-topic reading frameworks (most contributions land here)
└── scripts/              ← bridge.py only (pure-stdlib Python loopback bridge)
```

The skill follows the [Agent Skills specification](https://agentskills.io/specification). Before contributing, skim the spec's [frontmatter rules](https://agentskills.io/specification) and the design principles in [`SKILL.md`](skills/eastalmanac/SKILL.md).

## Ways to contribute

### Terminology corrections

The single source of truth is [`references/glossary.md`](skills/eastalmanac/references/glossary.md). If a term is mistranslated, a mapping table is wrong, or a definition is unclear, fix it there — **don't** duplicate the fix in a topic reference.

### New topic references

Want to add a new reading topic (e.g. 六爻, 紫微斗数, 塔罗)? Open an issue first to discuss scope, then:

1. Create `references/<topic>.md` following the existing pattern:
   - `## Step 0 — Gather Inputs` (plain-language questions, infer-then-ask)
   - `## Data Source` (EastAlmanac bridge page (`python3 scripts/bridge.py ...`))
   - `## Analysis Framework` (the professional reading structure)
   - `## Output` with **two layers**: inner (命理要点, terms OK) + outer (大白话总结, plain language)
2. Add a row to the routing table in [`SKILL.md`](skills/eastalmanac/SKILL.md).
3. Cross-link from related references (e.g. a new `liuyao.md` should point to `glossary.md`).

### Translations / language improvements

The skill auto-detects the user's language and replies in kind. If the plain-language delivery rules or the glossary translations can be improved for a specific language, edit the relevant section.

### Bug fixes in the bridge script

[`scripts/bridge.py`](skills/eastalmanac/scripts/bridge.py) must stay pure standard library (no pip dependencies) and work on any preinstalled Python 3. Smoke-test all three actions without opening a browser:

```bash
BROWSER=/usr/bin/true python3 skills/eastalmanac/scripts/bridge.py cast --question=test   # then Ctrl-C, or POST to the printed callback URL
```

All real calculation happens client-side on `eastalmanac.com` — never add local computation engines to this repo.

## Authoring rules

These keep the skill effective and the context window lean:

- **SKILL.md must stay under 500 lines.** Push detail into `references/`.
- **References stay one level deep** (`references/foo.md`, not `references/sub/foo.md`).
- **DRY** — terminology lives in `glossary.md`; mapping tables live in `mapping-tables.md`. Other references link, never copy.
- **Every output ends in plain language** — the outer layer is mandatory (see the *Two-Layer Output* principle in `SKILL.md`).
- **Infer before asking** — don't add a clarifying question to a `Step 0` if the input's wording already reveals the answer.

## Frontmatter

If you touch `SKILL.md`, validate the frontmatter:

- `name` must be lowercase `eastalmanac`, matching the directory name
- `description` ≤ 1024 characters, describes *what* and *when to use*
- `license` and `compatibility` are present
- `metadata.version` follows [SemVer](https://semver.org): bump PATCH for fixes, MINOR for new topics, MAJOR for breaking changes

## Submitting changes

1. Fork the repo and create a branch: `git checkout -b fix/glossary-typo`
2. Commit with a clear message: `fix: correct 食神 definition in glossary` / `feat: add liuyao reading reference`
3. Open a pull request describing what changed and why.

For terminology or factual corrections, include a source (classical text, established reference) in the PR description.

## Code of conduct

Be respectful and constructive. Fortune-telling traditions have many schools and regional variants — disagree without dismissing.
