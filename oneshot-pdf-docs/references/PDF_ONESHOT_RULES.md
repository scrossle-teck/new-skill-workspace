# PDF-specific ONESHOT rules & tips

- Use `pdfplumber` or `pypdf` to extract text and tables.
- Preserve code fences exactly as they appear in the PDF where possible.
- Extract tables to Markdown using the header + separator row pattern.
- If the PDF contains multi-column layouts, extract paragraphs in reading order when possible; otherwise, flag for manual review.
- Create an intermediate TXT to feed into the existing TXT chunker to ensure identical downstream rules.
- Include page numbers in `source` front-matter when useful for traceability.
