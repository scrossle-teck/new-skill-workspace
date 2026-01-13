---
name: python-usage
description:
  Best practices for Python development, including virtual environments,
  dependency management, and code quality tools.
---

# Python Usage

## Best Practices for Python Development

### 1. Use a Virtual Environment

A virtual environment ensures that your Python dependencies are isolated from
the system Python installation. This prevents version conflicts and makes your
project more portable.

#### 1.1 Steps to Create and Activate a Virtual Environment

1. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:

   - On Windows:

     ```powershell
     .venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source .venv/bin/activate
     ```

3. Deactivate the virtual environment when done:

   ```bash
   deactivate
   ```

### 2. Manage Dependencies with `pip` and `requirements.txt`

Use `pip` to install and manage dependencies, and maintain a `requirements.txt`
file to track them.

#### 2.1 Commands

- Install a package:

  ```bash
  pip install <package-name>
  ```

- Save installed packages to `requirements.txt`:

  ```bash
  pip freeze > requirements.txt
  ```

- Install packages from `requirements.txt`:

  ```bash
  pip install -r requirements.txt
  ```

### 3. Keep Python Updated

Ensure you are using a supported version of Python. Check your Python version:

```bash
python --version
```

### 4. Use Linters and Formatters

- **Linter**: Use `flake8` or `ruff` to check for code quality issues.
- **Formatter**: Use `black` to format your code consistently.

#### 4.1 Installation

```bash
pip install flake8 black
```

#### 4.2 Usage

- Lint your code:

  ```bash
  flake8 .
  ```

- Format your code:

  ```bash
  black .
  ```

### 5. Write Tests

Use `pytest` to write and run tests for your code.

#### 5.1 Installation

```bash
pip install pytest
```

#### 5.2 Running Tests

```bash
pytest
```

### 6. Document Your Code

Write clear docstrings for your functions and classes. Use tools like `pdoc` or
`Sphinx` to generate documentation.

### 7. Version Control with Git

Use Git to track changes in your project. Initialize a Git repository:

```bash
git init
```

### 8. Use `.gitignore`

Add a `.gitignore` file to exclude unnecessary files from version control.
Example:

```ini
# Python
__pycache__/
*.py[cod]
.venv/
```

### 9. Stay Secure

- Avoid hardcoding sensitive information (e.g., API keys). Use environment
  variables instead.
- Use `pip-audit` to check for vulnerabilities in your dependencies:

  ```bash
  pip install pip-audit
  pip-audit
  ```

### 10. Read the Documentation

Refer to the [official Python documentation](https://docs.python.org/3/) for
detailed guidance on Python features and libraries.

## Editor & Linting Guidance for Skill Scripts

When authoring or patching scripts for skills (small utilities, extractors, packagers), we observed a recurring pattern of editor and linter issues. Apply these practices to keep code clean, typed, and editor-friendly:

- **Use type annotations**: Add parameter and return type annotations to all top-level functions. This helps Pylance/pyright and improves maintainability.

  - Example: `def slugify(s: str, maxlen: int = 60) -> str:`

- **Prefer explicit `typing` imports**: Use `List`, `Dict`, `Optional`, and `cast` where appropriate to help static checkers understand dynamic data (PDF extraction results, JSON-like dicts).

- **Handle optional third-party imports gracefully**: For optional runtime-only libs (like `pdfplumber`, `tiktoken`), wrap imports in try/except and provide a helpful runtime error if missing. This avoids editor "import could not be resolved" noise.

- **Avoid unused imports and variables**: Remove `json` or other unused imports; linters will flag them. If an import is only used in type comments, import under `if TYPE_CHECKING:` or use string annotations.

- **Annotate local variables used by the type checker**: When building dicts or lists that the type checker will inspect (e.g., front-matter dicts), annotate with `Dict[str, Any]` or `List[str]` to reduce unknown-type warnings.

- **Use `cast()` for dynamically typed library outputs**: When a library returns `Any` (tables, parsed pages), use `cast(List[Any], tables)` before iterating so the checker understands element types.

- **Keep functions small and testable**: Break out discrete behaviors (slugify, chunking, front-matter generation, table-to-markdown conversion) into small functions. Add unit tests for each.

- **Run checks locally before committing**:

  ```bash
  # within the project's venv
  pip install -r oneshot-pdf-docs/requirements.txt
  pip install ruff mypy black
  ruff check .
  mypy -p oneshot_pdf_docs || true
  black --check .
  ```

- **Editor config suggestions** (VS Code):
  - Enable Pylance with `python.analysis.typeCheckingMode` set to `basic` or `strict` depending on the project.
  - Configure `python.linting.ruffEnabled` (or `flake8`) and `python.formatting.provider` to `black`.

Applying these guidelines reduces the iterative re-linting cycle and makes automated tooling (CI, editors) more reliable when writing skill scripts.

### Practical Templates

Use these small templates when writing or refactoring skill scripts.

- Optional third-party import pattern:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  import pdfplumber  # type: ignore

try:
  import pdfplumber  # runtime import
except Exception:
  pdfplumber = None

if pdfplumber is None:
  raise RuntimeError("pdfplumber is required; install requirements.txt")
```

- Using `cast()` for dynamic library outputs and local annotations:

```python
from typing import List, Any, cast

def extract_tables(page) -> List[List[str]]:
  tables = cast(List[Any], page.extract_tables() or [])
  md_tables: List[str] = []
  for t in tables:
    headers = cast(List[str], t[0])
    rows = cast(List[List[Any]], t[1:])
    # build markdown
    md_tables.append("| " + " | ".join(headers) + " |")
  return md_tables
```

- Small function typing and front-matter example:

```python
from typing import Dict, Any

def build_front_matter(title: str, typ: str) -> str:
  fm: Dict[str, Any] = {"title": title, "type": typ}
  lines = ["---"]
  for k, v in fm.items():
    lines.append(f"{k}: {v}")
  lines.append("---")
  return "\n".join(lines)
```

These templates are intentionally conservative — they aim to minimize editor warnings while preserving runtime flexibility.

## Editor Verification Checklist (for contributors and automated agents)

Before submitting changes or returning work, follow this checklist to reduce editor/CI noise and ensure a clean developer experience:

- **Open the VS Code Problems panel** and resolve or explicitly acknowledge all issues. Address high-severity problems first.
- **Run linters locally**:
  - `ruff check .` or `ruff check path/to/changed/files`
  - `mypy .` (or `mypy path/to/changed/files`)
- **Run formatter**: `black .` and re-run `ruff`/`mypy` after formatting.
- **Address editor import issues**: If the editor reports "Import could not be resolved" for optional dependencies, ensure the code uses `TYPE_CHECKING` or guards imports with try/except as shown in templates.
- **Fix or justify `type: ignore`**: Avoid leaving `# type: ignore` comments; if unavoidable, add a short explanatory comment about why it's necessary.
- **Run the project's quick checks** (script or command provided in SKILL) and confirm no new problems appear.

Agents and contributors should **explicitly confirm** (in their commit message or PR description) that they checked the VS Code Problems panel and ran the linters. This reduces churn where reviewers or CI discover obvious editor-reported issues.
