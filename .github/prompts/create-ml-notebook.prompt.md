---
description: "Scaffold a complete, self-contained ML notebook covering the full end-to-end pipeline for a given topic"
agent: agent
argument-hint: "Topic name, e.g. 'text classification with LSTM'"
tools: [read, edit, search]
---

You are scaffolding a **complete, single-notebook ML pipeline** for the topic provided by the user.

## Rules (Non-Negotiable)

1. The notebook must be **entirely self-contained** — one file, full flow, zero imports from other notebooks.
2. Follow all standards in [notebook-standards.instructions.md](../instructions/notebook-standards.instructions.md) and [python-standards.instructions.md](../instructions/python-standards.instructions.md).
3. All Python code must be executable inside WSL with `source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate`.
4. **Check `foundation/` first** — reuse any existing helpers rather than duplicating them.

## Required Notebook Structure

Generate cells in this exact order:

### Cell 1 — Title (Markdown)
```markdown
# <Topic> — End-to-End Pipeline
**Date**: <today's date>
**Objective**: <one-sentence goal>
**Dataset**: <dataset description>
```

### Cell 2 — Imports & Seeds (Code)
- All imports at the top
- Set all random seeds: `random`, `numpy`, `tensorflow`
- Print library versions for reproducibility

### Cell 3 — Configuration (Code)
- Paths using `pathlib.Path`
- Hyperparameters as typed constants
- No hardcoded values anywhere else in the notebook

### Cell 4 — Data Loading (Code + Markdown header)
### Cell 5 — EDA (Code + Markdown header)
### Cell 6 — Preprocessing (Code + Markdown header)
### Cell 7 — Model Definition (Code + Markdown header)
### Cell 8 — Training (Code + Markdown header)
### Cell 9 — Evaluation & Metrics (Code + Markdown header)
### Cell 10 — Visualization (Code + Markdown header)
### Cell 11 — Summary (Markdown)
Key results, metrics achieved, and next steps.

## Output

Save the notebook to `foundation/<slug-topic>.ipynb` where slug-topic is lowercase-hyphenated.
Confirm the file was created and list the cell count.
