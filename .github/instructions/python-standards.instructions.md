---
description: "Use when writing, reviewing, or generating Python code or Jupyter notebooks. Covers PEP 8, type hints, naming conventions, error handling, and enterprise quality standards."
applyTo: ["**/*.py", "**/*.ipynb"]
---

# Python Coding Standards

## Style & Formatting

- Follow **PEP 8** strictly: 4-space indentation, max 88-char lines (Black-compatible).
- Use `snake_case` for variables and functions, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants.
- Group imports: stdlib → third-party → local; separated by blank lines.

```python
# Good
import os
import sys

import numpy as np
import tensorflow as tf

from foundation.utils import load_data
```

## Type Hints (Required on All New Code)

```python
def tokenize_text(text: str, max_tokens: int = 512) -> list[str]:
    ...

def train_model(
    X_train: np.ndarray,
    y_train: np.ndarray,
    epochs: int = 10,
) -> tf.keras.Model:
    ...
```

## No Duplication — DRY Enforcement

- **Search before writing**: check existing helpers in `foundation/` before creating new utilities.
- Extract any logic used more than once into a named function.
- Never copy-paste code blocks; parameterize instead.

## Error Handling

- Validate only at system boundaries (file I/O, user input, external APIs).
- Use specific exceptions, never bare `except:`.
- Provide informative messages with context.
- Remove temporary debug `print()` statements, ad-hoc debug files, and one-off debug log lines after the issue is fixed.
- Keep only intentional production logs (structured and level-appropriate).

```python
# Good
try:
    data = np.load(file_path)
except FileNotFoundError as exc:
    raise FileNotFoundError(f"Dataset not found at {file_path}") from exc
```

## Functions & Classes

- Single responsibility: one function = one task.
- Keep functions under 30 lines; extract helpers if larger.
- Prefer pure functions; avoid global state.
- Use dataclasses or NamedTuple for structured data over raw dicts.
- Avoid leaving debug-only helper methods/functions once debugging is complete.

## ML-Specific Conventions

- Set random seeds at the top of every experiment: `np.random.seed(42)`, `tf.random.set_seed(42)`.
- Always separate data loading, preprocessing, training, and evaluation into distinct named functions.
- Log experiment parameters and metrics; never print raw loss without context.
- Save model artifacts with versioned names: `model_v1_epoch10.h5`.

## Quality Gates (Run Before Finishing)

```bash
# Run inside WSL
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; flake8 <file> --max-line-length 88; mypy <file>"
```
