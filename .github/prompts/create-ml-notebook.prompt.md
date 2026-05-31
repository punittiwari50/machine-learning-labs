---
description: "Scaffold a complete, self-contained ML notebook covering the full end-to-end pipeline for a given topic"
agent: agent
argument-hint: "Topic name, for example text classification with LSTM"
tools: [read, edit, search]
---

You are creating one complete notebook for the requested topic.

## Mission

Generate a single, runnable notebook with a full end-to-end ML flow.

## Required Structure

1. Title and objective.
2. Imports and random seed setup.
3. Configuration and constants.
4. Data loading.
5. EDA.
6. Preprocessing.
7. Model definition.
8. Training.
9. Evaluation and metrics.
10. Results visualization.
11. Summary.

## Rules

- Keep everything in one notebook file for the topic.
- Search existing helpers before creating duplicate logic.
- Follow workspace instruction files for notebook and Python standards.
- Keep paths portable and avoid absolute Windows paths.

## Output

- Save notebook to foundation/<kebab-case-topic>.ipynb.
- Report the created file path and total cell count.

## References

- ../instructions/notebook-standards.instructions.md
- ../instructions/python-standards.instructions.md
- ../instructions/policy.instructions.md
