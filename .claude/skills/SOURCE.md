# Source Attribution

The equity-research skills in this directory were copied from:

**Repository:** [anthropics/financial-services](https://github.com/anthropics/financial-services)
**Path:** `plugins/vertical-plugins/equity-research/skills/` and `commands/`
**License:** Apache-2.0
**Date copied:** 2026-06-24

## Skills included

| Skill | Command | Purpose |
|-------|---------|---------|
| `idea-generation` | `/screen` | Quantitative screens and thematic sweeps |
| `catalyst-calendar` | `/catalysts` | Upcoming catalyst tracking |
| `earnings-preview` | `/earnings-preview` | Pre-earnings scenario analysis |
| `earnings-analysis` | `/earnings` | Post-earnings update reports |
| `thesis-tracker` | `/thesis` | Investment thesis maintenance |

## What was NOT copied

- `initiating-coverage`, `model-update`, `morning-note`, `sector-overview` skills
- The `financial-analysis` core plugin and its MCP data connectors
- The `earnings-reviewer` and `market-researcher` agents

These skills run **connector-less** — they use web search and user-provided data only,
not paid financial data APIs.
