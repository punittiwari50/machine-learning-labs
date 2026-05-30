---
name: ml-notebook-scaffold
description: "Use when creating a new ML notebook or experiment from scratch. Guides through the complete end-to-end scaffold: imports, config, data, model, training, evaluation, visualization, summary. Enforces one-notebook one-complete-flow rule."
---

# ML Notebook Scaffold — Skill

## Purpose

This skill scaffolds a **complete, self-contained ML notebook** for any given topic. It enforces the workspace's one-notebook-one-flow rule and applies all Python and notebook standards.

## Trigger

Invoke this skill when the user says:
- "create a new notebook for..."
- "scaffold an ML experiment for..."
- "start a new lab on..."
- "build an end-to-end notebook for..."

## Steps

### Step 1 — Gather Requirements
Ask the user (or infer from context):
- Topic / algorithm name
- Dataset (built-in, file, or URL)
- Framework (TensorFlow/Keras, PyTorch, scikit-learn, etc.)
- Key hyperparameters to expose

### Step 2 — Check for Duplication
Search `foundation/` for any existing notebook on the same topic.  
If found: extend or improve it rather than creating a new one.

### Step 3 — Generate Notebook Structure
Use the [create-ml-notebook prompt](../../prompts/create-ml-notebook.prompt.md) to generate the full notebook with all required sections.

### Step 4 — Validate
- Verify all 10+ sections are present.
- Confirm random seeds are set.
- Confirm notebook runs top-to-bottom in WSL.

### Step 5 — Quality Check
Delegate to `code-quality` subagent for final audit.  
Fix all ❌ violations before completing.

## File Output Convention

`foundation/<lowercase-hyphenated-topic>.ipynb`

Examples:
- `foundation/text-classification-lstm.ipynb`
- `foundation/image-cnn-cifar10.ipynb`
- `foundation/transformer-attention-basics.ipynb`

## Standards Applied

- [python-standards.instructions.md](../../instructions/python-standards.instructions.md)
- [notebook-standards.instructions.md](../../instructions/notebook-standards.instructions.md)
- [wsl-execution.instructions.md](../../instructions/wsl-execution.instructions.md)
- [policy.instructions.md](../../instructions/policy.instructions.md)
