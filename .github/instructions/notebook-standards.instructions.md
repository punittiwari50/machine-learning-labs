---
description: "Use when creating or editing Jupyter notebooks (.ipynb). Enforces one-notebook one-complete-flow rule, cell structure, self-contained execution, and reproducibility standards."
applyTo: "**/*.ipynb"
---

# Notebook Standards

## One Notebook = One Complete Flow (Non-Negotiable)

Every notebook must be **fully self-contained** and cover the entire end-to-end pipeline:

```
Cell 1: Imports & Setup (all dependencies at the top)
Cell 2: Configuration & Constants (paths, hyperparameters, seeds)
Cell 3: Data Loading
Cell 4: Exploratory Data Analysis (EDA)
Cell 5: Preprocessing / Feature Engineering
Cell 6: Model Definition
Cell 7: Training
Cell 8: Evaluation & Metrics
Cell 9: Results Visualization
Cell 10: Summary / Conclusions
```

**Never** split a single topic across multiple notebooks.

## Reproducibility

- First code cell always sets all random seeds:

```python
import random, os
import numpy as np
import tensorflow as tf

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)
os.environ["PYTHONHASHSEED"] = str(SEED)
```

- Pin versions in a cell or `requirements.txt` reference.

## Cell Rules

- **Each cell has one responsibility** — don't mix data loading and model training.
- **All cells must run top-to-bottom** without errors on a fresh kernel restart.
- **No hidden state** — never rely on variables set in a cell that comes later.
- Keep cells short (< 50 lines). Extract helpers into functions within the notebook.

## Markdown Structure

Every notebook must have:
- A **title cell** (H1) with topic, date, and objective.
- **Section headers** (H2/H3) before each major stage.
- A **summary cell** at the end with key findings and metrics.

```markdown
# Topic Name — End-to-End Pipeline
**Date**: YYYY-MM-DD  
**Objective**: One sentence describing the goal.
```

## Execution

Run notebooks in WSL:

```bash
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; jupyter nbconvert --to notebook --execute <notebook>.ipynb"
```

## Anti-Patterns to Avoid

- Splitting preprocessing into a separate notebook and importing pickles.
- Leaving cells with errors or `[*]` execution state.
- Hardcoded absolute Windows paths — use `pathlib.Path` with relative paths.
- Multiple notebooks covering the same topic with slight variations.
