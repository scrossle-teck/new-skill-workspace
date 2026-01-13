# Condensed ONESHOT rules (extracted from the oneshot TXT)

- Single TXT input is canonical.
- Produce exactly one ZIP with a single top-level directory.
- README.md: human-facing, no front-matter.
- index.md: machine-facing, must include front-matter and `type: index`.
- Other files: exactly one atomic unit per file; must start with YAML front-matter.
- Normalize repeated boilerplate into `shared/common-concepts.md`.
- Preserve examples verbatim; do not invent or merge files.
- Target ~500-1200 tokens per file when feasible.
- Filenames must be exact symbolic identifiers.
