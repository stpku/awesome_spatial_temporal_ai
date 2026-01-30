# AGENTS.md

This repository is an Awesome List for Spatio-Temporal AI resources. Read this before contributing code.

## Build/Validate/Test Commands

### Validation
```bash
# Run full data validation (checks all JSON files in awesomelist/)
python validate_data.py

# Validate specific JSON syntax
python -c "import json; [json.load(open(f)) for f in ['awesomelist/{}.json'.format(x) for x in ['github_projects', 'latest_projects', 'conferences', 'journals', 'media_channels']]]"
```

### Metrics & Reporting
```bash
# Generate metrics summary and badges (outputs to docs/reports/)
python scripts/metrics.py

# Check all links (outputs to docs/reports/broken_links.json)
python scripts/linkcheck.py
```

### Development Tools
```bash
# Update GitHub stars for projects (requires gh CLI)
python tools/update_stars.py

# Archive daily papers from external report directory
python scripts/archive_daily_papers.py
```

## Python Environment

- **Target version**: Python 3.11
- Dependencies: `jsonschema` (for schema validation)
- Install: `pip install jsonschema`

## Code Style Guidelines

### Imports & Formatting
- Use standard library imports first, then third-party
- Group imports: standard library → third-party → local
- No enforced linter/formatter (be consistent with existing code)

### Type Annotations
- Use type hints for function signatures: `def validate_github_projects(data: dict) -> list:`
- Optional types: `Optional[str]` or union types like `type: ["string", "null"]` in schemas
- Keep it simple - no complex generic types

### Naming Conventions
- Functions/variables: `snake_case` (e.g., `validate_github_projects`, `all_errors`)
- Classes: `PascalCase` (rarely used in this codebase)
- Constants: `UPPER_SNAKE_CASE` (e.g., `DATA_DIR`, `MAX_WORKERS`)

### Error Handling
- Use try/except for JSON parsing and I/O operations
- Print descriptive error messages with context: `f"{filename}: {e}"`
- Return early with error lists for validation functions
- Don't silently suppress exceptions unless documented

### File I/O Patterns
```python
# Reading JSON
with open(filepath, encoding="utf-8") as f:
    data = json.load(f)

# Writing JSON
json.dump(data, f, indent=2, ensure_ascii=False)

# Use pathlib for paths
from pathlib import Path
DATA_DIR = Path("awesomelist")
filepath = DATA_DIR / "github_projects.json"
```

### Function Design
- Add docstrings to all functions: `"""Validate github_projects.json"""`
- Return structured data (lists of errors, tuples of (errors, warnings))
- Keep functions focused and under 50 lines when possible

### JSON Schema Validation
- Schemas are in `schemas/` directory (e.g., `github_projects.schema.json`)
- Use `jsonschema` package for validation
- Schema pattern: `format: "uri"`, `pattern: "^\\d{4}-\\d{2}-\\d{2}$"`

### Date Format
- Standard format: `YYYY-MM-DD` (e.g., `"2026-01-30"`)
- Parse: `datetime.strptime(s, "%Y-%m-%d")`
- Format: `datetime.strftime("%Y-%m-%d")`

### URL Validation
- Must start with `http://` or `https://`
- Validate in schemas: `"format": "uri"`
- Code check: `url.startswith(("http://", "https://"))`

### Concurrency
- Use `concurrent.futures.ThreadPoolExecutor` for I/O-bound tasks
- Pattern from linkcheck.py:
```python
with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
    futs = {ex.submit(check_url, url): (filename, name, url) for ...}
    for fut in concurrent.futures.as_completed(futs):
        ...
```

## Data File Structure

All data files are in `awesomelist/` directory:
- `github_projects.json` - categorized projects with stars
- `latest_projects.json` - cutting-edge research projects
- `conferences.json` - academic conferences
- `journals.json` - academic journals (international + chinese sections)
- `datasets.json` - research datasets
- `media_channels.json` - wechat_publications + newsletters
- `papers.json` - academic papers

Schema files in `schemas/` validate each JSON structure.

## Contributing

1. Add/edit data in `awesomelist/*.json`
2. Run `python validate_data.py` to check syntax and schema compliance
3. Test links with `python scripts/linkcheck.py`
4. Update metrics with `python scripts/metrics.py`
5. Commit changes with descriptive messages

## Architecture (New)

The project now uses a modular plugin-based architecture:

### Directory Structure
```
src/
├── core/               # Shared infrastructure
│   ├── config.py      # Configuration management
│   ├── io.py          # JSON I/O utilities
│   └── logger.py      # Logging utilities
└── validators/         # Plugin-based validators
    ├── base.py        # BaseValidator abstract class
    ├── registry.py    # Validator registry
    ├── github_projects.py
    ├── latest_projects.py
    ├── conferences.py
    ├── journals.py
    ├── datasets.py
    ├── media_channels.py
    └── papers.py
```

### Using the New Architecture

```python
# Import from src package
from src.core import Config, load_json, Logger
from src.validators.registry import ValidatorRegistry

# Use validator registry
registry = ValidatorRegistry()
validator = registry.get_validator("github_projects.json")
errors = validator.validate(data)
```

### Adding a New Validator

1. Create a new file in `src/validators/`:
```python
from typing import List
from .base import BaseValidator

class MyDataValidator(BaseValidator):
    @property
    def filename(self) -> str:
        return "my_data.json"
    
    @property
    def name(self) -> str:
        return "My Data"
    
    def validate(self, data: dict) -> List[str]:
        errors = []
        # Your validation logic here
        return errors
```

2. Register in `src/validators/registry.py`:
```python
from .my_data import MyDataValidator
# Add to validators list
validators = [
    # ... existing validators
    MyDataValidator(),
]
```

## Notes

- No automated tests exist - validation serves as testing
- GitHub Actions run validation on push/PR to `awesomelist/*.json`
- Soft-fail domains for link checking: `ieeexplore.ieee.org`, `mdpi.com`, `elsevier.com`, `springer.com`
- Use `gh` CLI for GitHub API calls (stars update)
- New modular architecture in `src/` package (backward compatible)
