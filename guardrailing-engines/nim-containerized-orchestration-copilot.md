# Copilot Workflow - NVIDIA NIM Containerized Engine Orchestration

## Objective

Run and validate separate guardrail notebook flows for NVIDIA NIM containerized
orchestration types.

## Notebook Types

- `nim-compose-orchestration-guardrails.ipynb`
- `nim-kubernetes-orchestration-guardrails.ipynb`
- `nim-multi-engine-routing-guardrails.ipynb`

Each type is isolated in its own notebook and markdown file for independent
review, testing, and release-gate checks.

## Recommended Agent Sequence

1. `@ML Lab`: implement and refine notebook logic.
2. `@Code Quality`: run read-only standards and policy audit.
3. `@ML Integration Architect`: map notebooks to service boundaries and deploy.
4. `@ML CI/CD Release Engineer`: enforce canary and rollback release gates.

## Verification Commands

Run each notebook in WSL Ubuntu with the workspace environment:

```bash
C:/Windows/System32/wsl.exe -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; jupyter nbconvert --to notebook --execute guardrailing-engines/nim-compose-orchestration-guardrails.ipynb --output nim-compose-orchestration-guardrails_tested.ipynb --output-dir guardrailing-engines/tested"
C:/Windows/System32/wsl.exe -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; jupyter nbconvert --to notebook --execute guardrailing-engines/nim-kubernetes-orchestration-guardrails.ipynb --output nim-kubernetes-orchestration-guardrails_tested.ipynb --output-dir guardrailing-engines/tested"
C:/Windows/System32/wsl.exe -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; jupyter nbconvert --to notebook --execute guardrailing-engines/nim-multi-engine-routing-guardrails.ipynb --output nim-multi-engine-routing-guardrails_tested.ipynb --output-dir guardrailing-engines/tested"
```

## Delivery Criteria

- All notebook cells execute top-to-bottom on a fresh kernel.
- Guardrail metrics are generated for each type.
- Tested outputs are written to `guardrailing-engines/tested/`.
- Rollback and canary signals are present in each summary section.
