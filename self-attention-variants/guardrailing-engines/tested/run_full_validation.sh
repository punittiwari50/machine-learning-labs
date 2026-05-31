#!/usr/bin/env bash

source ~/.bashrc_dev
source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate

set -euo pipefail

REPO_ROOT="/mnt/c/DEV/PROJECTS/ML_BASICS/machine-learning-labs"
TEST_DIR="${REPO_ROOT}/self-attention-variants/guardrailing-engines/tested"
SWEEP_SCRIPT="${TEST_DIR}/run_guardrail_nb_sweep.sh"

cd "${REPO_ROOT}"
mkdir -p "${TEST_DIR}"

TS="$(date +%Y%m%d-%H%M%S)"
REPORT="${TEST_DIR}/validation-report-${TS}.md"
LATEST="${TEST_DIR}/validation-report-latest.md"

run_and_capture() {
    local label="$1"
    local cmd="$2"
    local out_file="$3"

    echo "[RUN] ${label}"
    if bash -lc "${cmd}" >"${out_file}" 2>&1; then
        echo "[PASS] ${label}"
        return 0
    fi

    echo "[FAIL] ${label}"
    return 1
}

FLAKE8_OUT="/tmp/flake8_full_${TS}.log"
MYPY_OUT="/tmp/mypy_full_${TS}.log"
SWEEP_OUT="/tmp/nb_sweep_${TS}.log"

FLAKE8_STATUS="PASS"
MYPY_STATUS="PASS"
SWEEP_STATUS="PASS"

if ! run_and_capture "flake8 (full workspace)" "cd '${REPO_ROOT}'; flake8 ." "${FLAKE8_OUT}"; then
    FLAKE8_STATUS="FAIL"
fi

if ! run_and_capture "mypy (full workspace)" "cd '${REPO_ROOT}'; mypy . --ignore-missing-imports" "${MYPY_OUT}"; then
    MYPY_STATUS="FAIL"
fi

if ! run_and_capture "guardrailing notebook sweep" "'${SWEEP_SCRIPT}'" "${SWEEP_OUT}"; then
    SWEEP_STATUS="FAIL"
fi

{
    echo "# Full Validation Report"
    echo
    echo "- Date: $(date -Is)"
    echo "- Scope: flake8 + mypy + guardrailing notebook sweep"
    echo
    echo "## Status"
    echo "- flake8: ${FLAKE8_STATUS}"
    echo "- mypy: ${MYPY_STATUS}"
    echo "- notebook_sweep: ${SWEEP_STATUS}"
    echo
    echo "## flake8 output (tail)"
    echo '```text'
    tail -n 80 "${FLAKE8_OUT}" || true
    echo '```'
    echo
    echo "## mypy output (tail)"
    echo '```text'
    tail -n 80 "${MYPY_OUT}" || true
    echo '```'
    echo
    echo "## notebook sweep output (tail)"
    echo '```text'
    tail -n 120 "${SWEEP_OUT}" || true
    echo '```'
} >"${REPORT}"

cp "${REPORT}" "${LATEST}"

echo "REPORT_PATH:${REPORT}"
echo "LATEST_PATH:${LATEST}"

if [[ "${FLAKE8_STATUS}" == "FAIL" || "${MYPY_STATUS}" == "FAIL" || "${SWEEP_STATUS}" == "FAIL" ]]; then
    exit 1
fi
