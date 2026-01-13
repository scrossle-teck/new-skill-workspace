#!/usr/bin/env python3
"""End-to-end PDF -> TXT extraction -> TXT chunking -> Markdown docs -> ZIP.

This file is a prototype. It:
- calls the PDF extractor to produce an intermediate TXT
- runs a conservative TXT->atomic-Markdown chunker (prototype heuristics)
- writes a single top-level <base>-docs/ folder with README.md, index.md,
  shared/common-concepts.md, and atomic .md files
- calls the existing oneshot-llm-docs packager to validate and create the ZIP

Notes:
- This is a prototype; heuristics are conservative and intended for review.
"""

import sys
import os
import re
from subprocess import run
from typing import List, Optional, Dict, Any, cast


def slugify(s: str, maxlen: int = 60) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:maxlen].rstrip("-")


def words(text: str) -> int:
    return len(re.findall(r"\w+", text))


def infer_type(chunk_text: str) -> str:
    # crude heuristics
    if re.search(r"^\s*(```|\$ )", chunk_text, re.M):
        return "reference"
    if re.search(r"\b(GET|POST|PUT|DELETE|PATCH)\b\s+\/", chunk_text):
        return "endpoint"
    if re.search(r"\w+\s*\(.*\)\s*\{", chunk_text):
        return "function"
    if re.search(r"(^|\n)Syntax:|^\w+\s+\-\-|^\$ ", chunk_text, re.M):
        return "command"
    return "concept"


def build_front_matter(
    title: str,
    typ: str,
    product: Optional[str] = None,
    vendor: Optional[str] = None,
    language: Optional[str] = None,
    domain: Optional[str] = None,
    source_title: Optional[str] = None,
    source_section: Optional[str] = None,
) -> str:
    fm: Dict[str, Any] = {
        "title": title,
        "type": typ,
    }
    if product:
        fm["product"] = product
    if vendor:
        fm["vendor"] = vendor
    if language:
        fm["language"] = language
    if domain:
        fm["domain"] = domain
    fm["llm_use"] = "reference" if typ in ("reference", "endpoint") else "procedural"
    fm["prerequisites"] = []
    fm["inputs"] = "none"
    fm["outputs"] = "none"
    fm["state_effect"] = "none"
    fm["tags"] = []
    fm["source"] = {
        "type": "PDF",
        "title": source_title or "",
        "section": source_section or "",
    }
    # render simple YAML block
    lines: List[str] = ["---"]
    for k, v in fm.items():
        if isinstance(v, list):
            lines.append(f"{k}:")
            for item in cast(List[Any], v):
                lines.append(f"  - {item}")
        elif isinstance(v, dict):
            lines.append(f"{k}:")
            for kk, vv in cast(Dict[str, Any], v).items():
                lines.append(f"  {kk}: {vv}")
        else:
            lines.append(f"{k}: {v}")
    lines.append("---\n")
    return "\n".join(lines)


def split_into_paragraphs(txt: str) -> List[str]:
    # Normalize and split on two or more newlines
    parts = re.split(r"\n\s*\n", txt)
    return [p.strip() for p in parts if p.strip()]


def chunk_paragraphs(
    paragraphs: List[str], min_words: int = 200, target_words: int = 800
) -> List[str]:
    chunks: List[str] = []
    cur: List[str] = []
    cur_words = 0
    for p in paragraphs:
        pw = words(p)
        # never split inside code fence: keep fence as single paragraph
        cur.append(p)
        cur_words += pw
        if cur_words >= target_words:
            chunks.append("\n\n".join(cur))
            cur = []
            cur_words = 0
    if cur:
        chunks.append("\n\n".join(cur))
    # Merge very small chunks
    merged: List[str] = []
    for c in chunks:
        if merged and words(merged[-1]) < min_words:
            merged[-1] = merged[-1] + "\n\n" + c
        else:
            merged.append(c)
    return merged


def write_docs_folder(base: str, chunks: List[str], source_pdf: str) -> str:
    docs_dir = f"{base}-docs"
    if os.path.exists(docs_dir):
        # avoid clobbering by creating a new folder name
        i = 1
        while os.path.exists(f"{docs_dir}-{i}"):
            i += 1
        docs_dir = f"{docs_dir}-{i}"
    os.makedirs(docs_dir, exist_ok=True)
    # README.md (human) - do NOT include front-matter
    readme = (
        f"This documentation was generated from {os.path.basename(source_pdf)}.\n\n"
        "It contains atomic Markdown files intended for LLM-friendly retrieval.\n\n"
        "Files are split into small, atomic units; review before production.\n"
    )
    with open(os.path.join(docs_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme)

    # shared/common-concepts.md (stub)
    shared_dir = os.path.join(docs_dir, "shared")
    os.makedirs(shared_dir, exist_ok=True)
    with open(
        os.path.join(shared_dir, "common-concepts.md"), "w", encoding="utf-8"
    ) as f:
        f.write(
            "# Common Concepts\n\nThis file contains normalized boilerplate extracted from the source.\n"
        )

    # Write atomic files
    file_list: List[str] = []
    for i, c in enumerate(chunks, start=1):
        # derive title from first line or first 6 words
        first_line = c.split("\n", 1)[0].strip()
        title = (
            first_line if len(first_line) <= 80 else " ".join(first_line.split()[:6])
        )
        if not title:
            title = f"unit-{i}"
        slug = slugify(title)
        fname = f"{slug}.md"
        typ = infer_type(c)
        fm = build_front_matter(
            title=title,
            typ=typ,
            product=base,
            source_title=os.path.basename(source_pdf),
            source_section=f"chunk-{i}",
        )
        body = f"# {title}\n\n" + c + "\n"
        with open(os.path.join(docs_dir, fname), "w", encoding="utf-8") as f:
            f.write(fm)
            f.write(body)
        file_list.append(fname)

    # index.md (machine facing) with front-matter
    index_fm = {
        "title": f"{base} index",
        "type": "index",
        "product": base,
    }
    idx_lines: List[str] = ["---"]
    for k, v in index_fm.items():
        idx_lines.append(f"{k}: {v}")
    idx_lines.append("---\n")
    idx_lines.append("# Index\n\nThis file lists atomic units.\n")
    idx_lines.append("\n".join([f"- {fn}" for fn in file_list]))
    with open(os.path.join(docs_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(idx_lines))

    return docs_dir


def main(pdf_path: str) -> int:
    if not os.path.exists(pdf_path):
        print("PDF not found", file=sys.stderr)
        return 2
    base: str = os.path.splitext(os.path.basename(pdf_path))[0]
    tmp_txt: str = base + "-intermediate.txt"
    # call extractor (use sys.executable to preserve environment)
    extractor: str = os.path.join(os.path.dirname(__file__), "extract_pdf_text.py")
    rc = run([sys.executable, extractor, pdf_path, tmp_txt]).returncode
    if rc != 0:
        print("Extraction failed", file=sys.stderr)
        return rc

    # Read intermediate TXT and chunk
    with open(tmp_txt, "r", encoding="utf-8") as f:
        txt: str = f.read()
    paragraphs = split_into_paragraphs(txt)
    chunks = chunk_paragraphs(paragraphs)

    # write docs folder
    docs_dir = write_docs_folder(base, chunks, pdf_path)

    # call the local embedded packager to validate and zip
    packager = os.path.join(os.path.dirname(__file__), "package_docs_local.py")
    if not os.path.exists(packager):
        print("Local packager not found; created docs at", docs_dir)
        return 0
    rc = run([sys.executable, packager, docs_dir]).returncode
    if rc != 0:
        print("Packaging/validation failed; docs are in", docs_dir, file=sys.stderr)
        return rc
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: package_pdf_docs.py input.pdf")
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
