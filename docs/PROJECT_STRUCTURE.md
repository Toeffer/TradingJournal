# Project Structure

This repository is organized around a lightweight journal-first workflow.

## Core files

- `README.md` explains the project and setup flow.
- `AGENTS.md` defines how AI-assisted journaling should behave.
- `RISK_RULES.md` captures the written risk framework.
- `MONTHLY_SELF_GRADE.md` supports periodic review.
- `LLM_RESEARCH_PLAYBOOK.md` describes the research routine.

## Data folders

- `notes/` can hold longer narrative notes.
- `research/` can hold research outputs and candidate lists.
- `docs/` can hold project documentation.

## Future app structure

Once the implementation stack is chosen, add application code in clearly separated folders, for example:

- `frontend/` for the user interface
- `backend/` for the API and business logic
- `scripts/` for import, export, and reporting helpers
- `tests/` for automated checks
