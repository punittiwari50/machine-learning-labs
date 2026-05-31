# Machine Learning Labs — Copilot Instructions

This file is always loaded for this workspace and defines the global operating model.

## 1) Source of Truth and Precedence

Follow rules in this order when they conflict:

1. Active user task/request.
2. Matching file-scoped rules in `.github/instructions/*.instructions.md`.
3. This file (`.github/copilot-instructions.md`).
4. Agent and prompt files.

Use `.github/instructions/` as the canonical rule set; do not duplicate those rules in generated content.

## 2) Global Non-Negotiables

1. No duplicated logic; search and reuse existing helpers first.
2. Keep solutions strictly in-topic.
3. Python and Node commands run in WSL Ubuntu.
4. Docker/Compose/Kubernetes commands run on host Windows.
5. Notebooks are complete end-to-end flows in one file.
6. Architecture uses loose coupling (Protocol/ABC), cycle-free dependencies, and clear layers.
7. Every enterprise concept maps to a practical mini enterprise usage.
8. Never commit secrets, hardcoded credentials, or temporary debug artifacts.

## 3) Runtime and Device Policy

- Python venv: `~/APPS_VENV/python_venv/run_3_14_2`
- Runtime flag file: `configs/runtime.env` (fallback: `configs/runtime.env.example`)
- `USE_GPU=1` enables GPU-first mode; `USE_GPU=0` forces CPU fallback.

Command template:

```bash
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; <command>"
```

## 4) Standard Delivery Workflow

1. Read relevant instruction files for the target files.
2. Search existing code to avoid duplication.
3. Implement minimal, maintainable changes.
4. Run required verification checks.
5. Fix issues and re-run checks until green or blocked.

Minimum verification:

```bash
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; flake8 . --max-line-length 88 --exclude .git,__pycache__"
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; mypy . --ignore-missing-imports"
```

Notebook verification:

```bash
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; jupyter nbconvert --to notebook --execute <notebook>.ipynb --output <notebook>_tested.ipynb"
```

## 5) Agent and Prompt Map

### Primary execution agent
- `@ML Lab`: Day-to-day ML notebook/code tasks and implementation.

### Quality and review
- `@Code Quality` (subagent): Read-only code/notebook audit.

### End-to-end delivery pipeline
- `@ML Delivery Orchestrator`
- `@ML Research Specialist`
- `@ML System Design Engineer`
- `@ML Quality Reviewer`
- `@ML Integration Architect`
- `@ML CI/CD Release Engineer`
- `@ML E2E Delivery Validator`

### Prompts
- `/create-ml-notebook`
- `/code-quality-review`
- `/deep-research`
- `/system-design`

## 6) Reference Files

### Core instruction files
- `instructions/python-standards.instructions.md`
- `instructions/notebook-standards.instructions.md`
- `instructions/wsl-execution.instructions.md`
- `instructions/policy.instructions.md`
- `instructions/performance.instructions.md`
- `instructions/architecture.instructions.md`
- `instructions/microservices.instructions.md`
- `instructions/build-dependency-standards.instructions.md`

### Agent runbooks
- `agents/docs/agent-collaboration-sequence.md`
- `agents/docs/delivery-orchestrator-playbook.md`
- `agents/docs/cicd-release-playbook.md`
- `agents/docs/docker-sequence-runbook.md`
- `agents/docs/code-generation-documentation-standard.md`
