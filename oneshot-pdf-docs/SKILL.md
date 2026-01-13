---
name: oneshot-pdf-docs
description: Skill to convert a single authoritative PDF into a strict, LLM-optimized, chunked Markdown documentation ZIP following ONESHOT rules, with PDF-specific extraction and table handling.
---

# ONESHOT PDF LLM-Optimized Docs Skill

This skill adapts the ONESHOT TXT workflow to operate directly from a single authoritative PDF. It uses PDF extraction techniques to pull text, preserve code and table examples, and then follows the same strict chunking, front-matter, and packaging rules as the TXT-based skill.

When to use:

- You have a canonical technical PDF containing documentation that must be transformed into machine- and human-friendly Markdown.

Bundled resources:

- `scripts/extract_pdf_text.py` - extracts structured text and tables from a PDF into a normalized intermediate TXT.
- `scripts/package_pdf_docs.py` - validates front-matter and packages the docs into the required ZIP.
- `requirements.txt` - PDF extraction libs (pdfplumber/pypdf and pandas for table export).
- `references/PDF_ONESHOT_RULES.md` - PDF-specific rules and tips.
