#!/usr/bin/env python3
"""Local packager for ONESHOT LLM-optimized docs (embedded copy).

Validates README/index/front-matter and creates <root>-llm-optimized-docs.zip
"""

import sys
import os
import re
import zipfile
from typing import Pattern

FRONT_RE: Pattern[str] = re.compile(r"^---\n(.*?)\n---\n", re.S)


def has_frontmatter(path: str) -> bool:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read(10240)
    return bool(FRONT_RE.match(content))


def main(root_dir: str) -> int:
    if not os.path.isdir(root_dir):
        print("Usage: package_docs.py <root-directory>")
        return 2
    root_name: str = os.path.basename(os.path.normpath(root_dir))
    readme: str = os.path.join(root_dir, "README.md")
    index: str = os.path.join(root_dir, "index.md")
    if not os.path.exists(readme):
        print("ERROR: README.md missing")
        return 3
    if has_frontmatter(readme):
        print("ERROR: README.md must NOT contain front-matter")
        return 4
    if not os.path.exists(index):
        print("ERROR: index.md missing")
        return 5
    if not has_frontmatter(index):
        print("ERROR: index.md must contain front-matter")
        return 6
    # validate other md files
    for dirpath, _, files in os.walk(root_dir):
        for fn in files:  # type: str
            if not fn.lower().endswith(".md"):
                continue
            p = os.path.join(dirpath, fn)
            # skip top-level README and index files
            try:
                if os.path.samefile(p, readme):
                    continue
                if os.path.samefile(p, index):
                    continue
            except FileNotFoundError:
                # samefile may raise if files don't exist; skip comparison
                pass
            if not has_frontmatter(p):
                print(f"ERROR: {p} missing front-matter")
                return 7
    zipname: str = f"{root_name}-llm-optimized-docs.zip"
    with zipfile.ZipFile(zipname, "w", zipfile.ZIP_DEFLATED) as zf:
        for dirpath, _, files in os.walk(root_dir):
            for fn in files:
                absf = os.path.join(dirpath, fn)
                arcname: str = os.path.relpath(absf, os.path.dirname(root_dir))
                zf.write(absf, arcname)
    print(f"Created {zipname}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]) if len(sys.argv) > 1 else main("."))
