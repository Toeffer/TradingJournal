# Skill Attribution

The equity-research skills in this directory were copied from Anthropic's public
**`anthropics/financial-services`** repository:

- Source: https://github.com/anthropics/financial-services
- Path in source: `plugins/vertical-plugins/equity-research/skills/<name>/`
- Matching slash commands copied to `.claude/commands/` from
  `plugins/vertical-plugins/equity-research/commands/<name>.md`
- License: **Apache-2.0**

## Skills copied (unchanged from source)

| Skill | Slash command | Used by RESEARCH_BRIEF |
|-------|---------------|------------------------|
| `idea-generation`   | `/screen`           | Stage 1 — discovery / screening |
| `catalyst-calendar` | `/catalysts`        | Stage 1 — catalyst dates |
| `earnings-preview`  | `/earnings-preview` | Stage 2 — deep-dive (core) |
| `earnings-analysis` | `/earnings`         | Stage 2 — only if trading the post-earnings drift |
| `thesis-tracker`    | `/thesis`           | Pairs with the journal for multi-week holds |

## Deliberately NOT copied

- Skills `initiating-coverage`, `model-update`, `morning-note`, `sector-overview`
  (and their commands `initiate.md`, `model-update.md`, `morning-note.md`, `sector.md`)
  — not needed for this workflow.
- The `financial-analysis` core plugin and **any MCP data connectors** — this setup
  runs the skills **connector-less** on purpose (web search + manual verification only).
- The `earnings-reviewer` and `market-researcher` *agents* — they would try to own the
  whole workflow and collide with `RESEARCH_BRIEF.md`, which already orchestrates it.

The skill files are reproduced verbatim from the source so attribution and future
updates stay traceable. If you re-sync from upstream, replace the folders wholesale
and keep this note in step.
