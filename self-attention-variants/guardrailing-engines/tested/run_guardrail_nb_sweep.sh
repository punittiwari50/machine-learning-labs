#!/usr/bin/env bash

source ~/.bashrc_dev
source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate

set -euo pipefail

cd /mnt/c/DEV/PROJECTS/ML_BASICS/machine-learning-labs
mkdir -p self-attention-variants/guardrailing-engines/tested

PASS=0
FAIL=0

for nb in self-attention-variants/guardrailing-engines/*.ipynb; do
    base="${nb##*/}"
    base="${base%.ipynb}"
    out="${base}_tested.ipynb"
    log="/tmp/${base}_nb.log"

    echo "[RUN] ${nb}"
    if jupyter nbconvert --to notebook --execute "${nb}" --output "${out}" --output-dir self-attention-variants/guardrailing-engines/tested >"${log}" 2>&1; then
        echo "[PASS] ${nb}"
        PASS=$((PASS + 1))
    else
        echo "[FAIL] ${nb}"
        FAIL=$((FAIL + 1))
        tail -n 30 "${log}" || true
    fi

done

echo "NOTEBOOK_PASS:${PASS}"
echo "NOTEBOOK_FAIL:${FAIL}"

if [ "${FAIL}" -ne 0 ]; then
    exit 1
fi
