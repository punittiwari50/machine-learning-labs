---
description: "Audit a Python file or Jupyter notebook for code quality issues: duplication, standards violations, missing type hints, hardcoded values, and policy non-compliance"
agent: agent
argument-hint: "File or notebook path to review"
tools: [read, search]
---

You are performing a read-only quality audit on the requested file.

## Mission

Return concrete findings with clear severity, location, and fix direction.

## Audit Scope

1. Duplication and reuse gaps.
2. Python and notebook standards compliance.
3. Architecture and layering issues.
4. Performance anti-patterns.
5. Policy and security compliance.

## Output Format

Use this report structure:

1. Passed
2. Warnings
3. Violations
4. Summary with top three priority fixes

Each warning and violation must include file location (Cell N or line reference).

## Constraints

- Read-only. Do not modify files.
- Do not run code.
- Do not provide generic feedback without evidence.

## References

- ../instructions/policy.instructions.md
- ../instructions/python-standards.instructions.md
- ../instructions/notebook-standards.instructions.md
- ../instructions/architecture.instructions.md
- ../instructions/performance.instructions.md
