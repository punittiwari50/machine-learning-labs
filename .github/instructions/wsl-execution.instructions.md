---
description: "Use when running, verifying, testing, or executing any Python code or scripts. All execution must happen inside WSL Ubuntu with the correct virtual environment activated."
applyTo: "**"
---

# Execution Environment

This workspace uses a split runtime model:
- Python/Node development and execution in **WSL Ubuntu**.
- Docker/Compose/Kubernetes container runtime commands on **host Windows**.

All Python execution must happen inside **WSL Ubuntu** with the following setup:

```bash
wsl -d Ubuntu
source ~/.bashrc_dev
source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate
```

## Rules

- **Always** run Python and Node.js commands inside `wsl -d Ubuntu`.
- Before running any Python code or pip installs, source both files in order:
  1. `source ~/.bashrc_dev`
  2. `source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate`
- **Never** run Python commands directly in Windows PowerShell or CMD.
- **Never** run Node.js package management/build commands on host Windows for this workspace.
- Run `docker`, `docker compose`, `kubectl`, and `helm` from host Windows terminal (Docker daemon is on host).
- When chaining commands in a single terminal call, use `;` as the separator (not `&&`) inside WSL.

## Standard Command Template

```bash
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; <your-command>"
```

Host container command template:

```powershell
docker compose -f <compose-file>.yml config
kubectl apply --dry-run=client -f <k8s-manifest-or-dir>
```

## Common Commands

```bash
# Run a Python script
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; python my_script.py"

# Install a package
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; pip install <package>"

# Execute a notebook
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; jupyter nbconvert --to notebook --execute <notebook>.ipynb"

# Run linting
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; flake8 <file> --max-line-length 88"

# Node command in WSL
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; npm run test"

# Docker Compose validation on host
docker compose -f <compose-file>.yml config

# Kubernetes manifest validation on host
kubectl apply --dry-run=client -f <k8s-manifest-or-dir>
```

## Virtual Environment Details

| Property | Value |
|----------|-------|
| Distro | Ubuntu (WSL) |
| Venv path | `~/APPS_VENV/python_venv/run_3_14_2` |
| Python version | 3.14.2 |
| Activation script | `~/APPS_VENV/python_venv/run_3_14_2/bin/activate` |
| Dev env setup | `~/.bashrc_dev` |
| Container runtime | Docker Desktop on Windows host |
