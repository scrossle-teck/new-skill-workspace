#!/usr/bin/env python3
"""Extract text and tables from a PDF into a normalized TXT suitable
for the ONESHOT chunker.

This script uses `pdfplumber` for extraction and attempts to preserve
code fences and table structures in a markdown-friendly way.
"""

import sys
import os
import re
from typing import List, Any, cast, Optional
from types import ModuleType

# pdfplumber is an optional runtime dependency. Declare a module-typed
# variable that may be `None` at runtime, then import it in a guarded
# block. This keeps the editor happy and lets mypy know the variable
# can be absent.
pdfplumber: Optional[ModuleType]
try:
    import pdfplumber as _pdfplumber

    pdfplumber = _pdfplumber
except Exception:  # pragma: no cover - editor/runtime fallback
    pdfplumber = None

CODE_BLOCK_MARKER = "```"


def extract(pdf_path: str, out_txt: str) -> int:
    """Extract text and tables from `pdf_path` and write to `out_txt`.

    Returns 0 on success, non-zero on error.
    """
    if not os.path.exists(pdf_path):
        print("PDF not found", file=sys.stderr)
        return 2
    if pdfplumber is None:
        print("pdfplumber not available; install requirements.txt", file=sys.stderr)
        return 3
    pages_text: List[str] = []
    pdf_module = cast(Any, pdfplumber)
    with pdf_module.open(pdf_path) as pdf:
        # `pdf` has a .pages list; each `page` supports `.extract_text()` and `.extract_tables()`
        for page in cast(List[Any], pdf.pages):
            text: str = str(page.extract_text() or "")
            # Heuristic: keep code-like blocks that have monospace or indentation
            # pdfplumber doesn't preserve fonts reliably; detect by pattern
            text = re.sub(r"\r\n", "\n", text)
            pages_text.append(text)
            # Extract tables
            tables = cast(List[Any], page.extract_tables() or [])
            for t in tables:
                # convert table to markdown
                if t:
                    headers = cast(List[Any], t[0])
                    rows = cast(List[List[Any]], t[1:])
                    md = "\n" + "| " + " | ".join([str(h) for h in headers]) + " |\n"
                    md += "| " + " | ".join(["---"] * len(headers)) + " |\n"
                    for r in rows:
                        md += (
                            "| "
                            + " | ".join([str(x) if x is not None else "" for x in r])
                            + " |\n"
                        )
                    pages_text.append(md)
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("\n\n".join(pages_text))
    print(f"Wrote {out_txt}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: extract_pdf_text.py input.pdf output.txt")
        sys.exit(2)
    sys.exit(extract(sys.argv[1], sys.argv[2]))
