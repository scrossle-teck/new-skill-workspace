---
name: oneshot-llm-docs
description: Skill to convert a single authoritative TXT into a strict, LLM-optimized, chunked Markdown documentation ZIP following ONESHOT rules.
---

# ONESHOT LLM-Optimized Docs Skill

This skill implements the deterministic one-shot conversion workflow described in the provided ONESHOT TXT. Use when you need to transform a single authoritative TXT (technical documentation) into a structured, high-fidelity Markdown documentation set optimized for small LLMs and packaged as one ZIP.

When to use:

- You have a single TXT file containing canonical technical documentation.
- You require semantically lossless conversion with strict chunking and front-matter enforcement.
- You need a machine-oriented `index.md`, human-oriented `README.md`, and a `shared/common-concepts.md` for normalized boilerplate.

Outputs:

- A ZIP file named `<inferred-subject>-llm-optimized-docs.zip` containing a single top-level `<inferred-subject>-docs/` folder with the required structure.

Bundled resources:

- `scripts/package_docs.py` - helper to validate front-matter and create the ZIP.
- `references/ONESHOT_RULES.md` - condensed rules extracted from the oneshot TXT for quick reference.
