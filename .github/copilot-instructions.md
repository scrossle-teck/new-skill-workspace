# Copilot / AI agent instructions for this repository

This file gives focused, actionable guidance so AI coding agents can be productive immediately.

**Repository Overview:**
- **Purpose:** A collection of small "skills" that transform input documents (TXT/PDF) into LLM-optimized Markdown packages and provide utility scripts for other workflows.
- **Top-level layout:** `oneshot-llm-docs/`, `oneshot-pdf-docs/`, `python/`, and `scripts/`.
- **Key entry points:** [oneshot-llm-docs/SKILL.md](oneshot-llm-docs/SKILL.md) and [oneshot-pdf-docs/SKILL.md](oneshot-pdf-docs/SKILL.md).

**High-level architecture & why it matters:**
- Each skill is self-contained: a `SKILL.md` describing intent, a `scripts/` folder with helpers, and a `references/` folder with rules.
- The ONESHOT workflow enforces deterministic outputs (single ZIP, exact filenames, YAML front-matter). Agents must preserve that determinism rather than introduce creative merges.

**Project-specific conventions (must follow):**
- ONESHOT rules: see [oneshot-llm-docs/references/ONESHOT_RULES.md](oneshot-llm-docs/references/ONESHOT_RULES.md).
- `index.md` is machine-facing and MUST include YAML front-matter containing `type: index`.
- `README.md` is human-facing and MUST NOT have front-matter.
- Every other content file must begin with YAML front-matter (metadata) and contain one atomic unit of content.
- Filenames are symbolic identifiers and should be exact (do not create fuzzy or natural-language names).
- Target ~500–1200 tokens per content file when chunking documents.

**Scripts & integration points:**
- Use [oneshot-llm-docs/scripts/package_docs.py](oneshot-llm-docs/scripts/package_docs.py) to validate front-matter and produce the ZIP for the LLM-docs workflow.
- Use [oneshot-pdf-docs/scripts/extract_pdf_text.py](oneshot-pdf-docs/scripts/extract_pdf_text.py) and [oneshot-pdf-docs/scripts/package_pdf_docs.py](oneshot-pdf-docs/scripts/package_pdf_docs.py) for PDF extraction and packaging.
- PDF work requires additional deps: see [oneshot-pdf-docs/requirements.txt](oneshot-pdf-docs/requirements.txt).

**Developer workflows (commands/examples):**
- Create and activate a venv, then install deps (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r oneshot-pdf-docs/requirements.txt
```

- Validate / package docs (example):

```powershell
python oneshot-llm-docs/scripts/package_docs.py --input input.txt --out out.zip
```

**Style & linting:**
- Project uses `black`, `ruff`, and `isort` configured in `pyproject.toml`. Target Python 3.10 formatting and lint rules.

**Agent best-practices (concrete rules):**
- Always run the project's packaging/validation script after generating docs to ensure strict front-matter and filenames.
- Never invent examples or merge distinct files; preserve verbatim examples from the canonical source.
- When chunking, enforce the token size range above and keep semantic boundaries intact.
- Use exact ZIP naming convention: `<inferred-subject>-llm-optimized-docs.zip` for TXT workflow and `<inferred-subject>-docs/` as top-level folder inside the ZIP.
- If you modify or add a `SKILL.md`, keep the YAML at the top (name/description) consistent with existing files.

**What not to do:**
- Do not add front-matter to `README.md` files.
- Do not change the ONESHOT semantics (single ZIP, single top-level folder).

If anything in this guidance is unclear or incomplete, ask for the specific example (input TXT/PDF and desired output) and I will iterate.
