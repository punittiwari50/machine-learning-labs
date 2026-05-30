---
description: "Audit a Python file or Jupyter notebook for code quality issues: duplication, standards violations, missing type hints, hardcoded values, and policy non-compliance"
agent: agent
argument-hint: "File or notebook path to review, e.g. 'foundation/04-embeddings-detailed-guide.ipynb'"
tools: [read, search]
---

You are performing a **read-only code quality audit** on the file or notebook provided. Do NOT modify any files.

## Audit Checklist

Run through each category and report findings with file and line/cell references.

### 1. Duplication
- [ ] Any function, logic block, or data pipeline duplicated elsewhere in the workspace?
- [ ] Any utility recreated that already exists in `foundation/`?
- [ ] Copy-pasted cells or code blocks that should be extracted?

### 2. Python Standards (PEP 8 + Type Hints)
- [ ] Functions missing type hints on parameters or return type?
- [ ] Variable names not following `snake_case`?
- [ ] Lines exceeding 88 characters?
- [ ] Bare `except:` clauses without specific exception types?
- [ ] Unused imports?

### 3. Notebook Completeness (for .ipynb only)
- [ ] Does the notebook have all required sections (imports → config → data → model → eval → results → summary)?
- [ ] Does it run top-to-bottom without errors on a fresh kernel restart?
- [ ] Are random seeds set at the top?
- [ ] Are there cells in error state?

### 4. Policy Compliance
- [ ] Hardcoded absolute paths or Windows-style paths?
- [ ] Credentials or API keys in plain text?
- [ ] TODO comments left in code?
- [ ] Missing `requirements.txt` entries for new dependencies?

## Output Format

Return a structured report:

```
## Quality Audit Report — <filename>

### ✅ Passed
- <item>

### ⚠️ Warnings
- <item> (Cell N / Line N): <description>

### ❌ Violations
- <item> (Cell N / Line N): <description> — Suggested fix: <fix>

### Summary
- Total violations: N
- Total warnings: N
- Recommended priority fixes: <top 3>
```
