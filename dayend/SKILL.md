---
name: dayend
description: Generate end-of-day artifacts (ASKS.md, CONVERSATION.md, SUMMARY.md, NEXTSTEPS.md) from current workspace context. Invoke when asking the assistant to summarize work, decisions, and open items for the day.
---

# Dayend Skill

This skill generates four artifacts from the current session context. See `references/automation.md` for the assistant invocation contract and `references/playbook.md` for examples.

Templates live in `templates/` and are substituted using `{transcript}`, `{date}`, `{user}`, and `{project}`.

## Quickstart (assistant-driven)

Create a transcript file (markdown) containing the full session.

Use the `prompt_template.txt` as a helper for assist invocation. You can say: "Run the `dayend` skill for project `infra` on `2026-01-15` and include open editors and recent git diffs." The assistant will follow the `assistant-invocation.md` contract and return the four files as code blocks with filenames.
