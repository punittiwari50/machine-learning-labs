from __future__ import annotations

import json
import os
from datetime import date
from pathlib import Path
from uuid import uuid4

BASE = Path("guardrailing-engines")
README = BASE / "README.md"
TODAY = date.today().isoformat()


def parse_sections(md_text: str) -> dict[str, list[str] | str]:
    lines = md_text.splitlines()
    sections: dict[str, list[str] | str] = {
        "title": lines[0].lstrip("# ").strip() if lines else "Guardrails",
        "scope": "",
        "core_controls": [],
        "validation_signals": [],
        "use_cases": [],
    }

    current = None
    for raw in lines:
        line = raw.strip()
        if line.lower() == "## scope":
            current = "scope"
            continue
        if line.lower() == "## core controls":
            current = "core_controls"
            continue
        if line.lower() == "## validation signals":
            current = "validation_signals"
            continue
        if line.lower() == "## realtime enterprise use cases":
            current = "use_cases"
            continue
        if line.startswith("## "):
            current = None
            continue
        if not line:
            continue

        if current == "scope" and not sections["scope"]:
            sections["scope"] = line
        elif current in {"core_controls", "validation_signals"} and line.startswith(
            "- "
        ):
            cast_list = sections[current]
            assert isinstance(cast_list, list)
            cast_list.append(line[2:].strip())
        elif current == "use_cases" and (line[0].isdigit() or line.startswith("-")):
            cast_list = sections["use_cases"]
            assert isinstance(cast_list, list)
            cast_list.append(line)

    return sections


def parse_agent_workflow(readme_text: str) -> list[str]:
    lines = readme_text.splitlines()
    out: list[str] = []
    in_block = False
    for raw in lines:
        line = raw.strip()
        if line.lower() == "## agent workflow":
            in_block = True
            continue
        if in_block and line.startswith("## "):
            break
        if in_block and line[:1].isdigit():
            out.append(line)
    return out


def make_cell_id() -> str:
    return uuid4().hex[:8]


def mk_markdown_cell(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": make_cell_id(),
        "metadata": {},
        "source": [line + "\n" for line in source.strip().splitlines()],
    }


def mk_code_cell(source: str) -> dict:
    return {
        "cell_type": "code",
        "id": make_cell_id(),
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": [line + "\n" for line in source.strip().splitlines()],
    }


def build_notebook(
    title: str,
    scope: str,
    guardrail_slug: str,
    core_controls: list[str],
    validation_signals: list[str],
    use_cases: list[str],
    agent_steps: list[str],
) -> dict:
    objective = (
        f"Build and validate automated benchmarking metrics for {title.lower()}."
    )

    summary_lines = [
        "- Validation signals tracked: "
        + (
            ", ".join(validation_signals)
            if validation_signals
            else "standard guardrail KPI set"
        )
        + ".",
        "- Core controls represented: "
        + (
            ", ".join(core_controls)
            if core_controls
            else "rule-based guardrail controls"
        )
        + ".",
        "- Automated benchmark metrics: mean latency, p95 latency,"
        " and throughput.",
        "- Tests executed in-notebook with assertion gates"
        " for quality and performance.",
        "- Agent workflow alignment:",
    ]
    summary_lines.extend([f"  {step}" for step in agent_steps])

    cells = [
        mk_markdown_cell(f"""
# {title} — End-to-End Pipeline
**Date**: {TODAY}
**Objective**: {objective}

**Scope**: {scope}
"""),
        mk_markdown_cell("## 1) Imports and Setup"),
        mk_code_cell(f"""
from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
import os
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
os.environ[\"PYTHONHASHSEED\"] = str(SEED)

try:
    import tensorflow as tf
except ImportError:
    tf = None

if tf is not None:
    tf.random.set_seed(SEED)


def parse_use_gpu_flag(raw_value: str) -> bool:
    normalized = raw_value.strip().lower()
    return normalized not in {{\"0\", \"false\", \"no\", \"off\"}}


USE_GPU = parse_use_gpu_flag(os.getenv(\"USE_GPU\", \"1\"))

try:
    import torch
except ImportError:
    torch = None

RUNTIME_DEVICE = (
    \"cuda\"
    if USE_GPU and torch is not None and torch.cuda.is_available()
    else \"cpu\"
)

print(
    f\"guardrail_type={guardrail_slug} | \"
    f\"USE_GPU={{int(USE_GPU)}} | runtime_device={{RUNTIME_DEVICE}}\"
)
"""),
        mk_markdown_cell("## 2) Configuration and Constants"),
        mk_code_cell(f"""
@dataclass(frozen=True)
class GuardrailConfig:
    guardrail_type: str
    block_threshold: float
    escalate_threshold: float
    canary_delta_limit: float
    max_rollout_ring: str


CONFIG = GuardrailConfig(
    guardrail_type=\"{guardrail_slug}\",
    block_threshold=0.72,
    escalate_threshold=0.58,
    canary_delta_limit=0.02,
    max_rollout_ring=\"ring_2\",
)

CORE_CONTROLS = {core_controls!r}
VALIDATION_SIGNALS = {validation_signals!r}
USE_CASE_LINES = {use_cases!r}

RINGS = [\"ring_0\", \"ring_1\", \"ring_2\", \"ring_3\"]
ROW_COUNT = 300
"""),
        mk_markdown_cell("## 3) Data Loading"),
        mk_code_cell("""
risk = np.random.uniform(0.0, 1.0, ROW_COUNT)
policy_tags = np.random.choice(
    ["safe", "pii", "restricted", "toxic", "policy_edge"],
    size=ROW_COUNT,
    p=[0.44, 0.16, 0.14, 0.12, 0.14],
)
rollout_ring = np.random.choice(RINGS, size=ROW_COUNT, p=[0.45, 0.25, 0.20, 0.10])

raw_df = pd.DataFrame(
    {
        "prompt_id": np.arange(1, ROW_COUNT + 1),
        "risk_score": risk,
        "policy_tag": policy_tags,
        "rollout_ring": rollout_ring,
        "compliance_ok": np.random.choice([True, False], size=ROW_COUNT, p=[0.9, 0.1]),
        "canary_delta": np.random.uniform(0.0, 0.05, ROW_COUNT),
    }
)

raw_df["true_block"] = (
    (raw_df["risk_score"] >= 0.74)
    | (raw_df["policy_tag"].isin(["restricted", "toxic"]))
).astype(int)

raw_df.head(5)
"""),
        mk_markdown_cell("## 4) Exploratory Data Analysis (EDA)"),
        mk_code_cell("""
eda_summary = {
    "rows": int(raw_df.shape[0]),
    "block_rate": float(raw_df["true_block"].mean()),
    "avg_risk_score": float(raw_df["risk_score"].mean()),
    "policy_distribution": (
        raw_df["policy_tag"].value_counts(normalize=True).round(3).to_dict()
    ),
}
eda_summary
"""),
        mk_markdown_cell("## 5) Preprocessing and Feature Engineering"),
        mk_code_cell("""
work_df = raw_df.copy()
work_df["is_high_risk_tag"] = work_df["policy_tag"].isin(
    ["restricted", "toxic"]
).astype(int)
work_df["ring_index"] = work_df["rollout_ring"].str.extract(r"(\\d)").astype(int)
work_df["can_release_by_ring"] = (work_df["ring_index"] <= 2).astype(int)
work_df["signal_compliance"] = work_df["compliance_ok"].astype(int)
work_df.head(5)
"""),
        mk_markdown_cell("## 6) Model Definition"),
        mk_code_cell("""
def evaluate_guardrail(row: pd.Series, cfg: GuardrailConfig) -> dict[str, int | bool]:
    should_block = int(
        (row["risk_score"] >= cfg.block_threshold)
        or (row["is_high_risk_tag"] == 1)
    )
    should_escalate = int(
        (row["risk_score"] >= cfg.escalate_threshold)
        and (row["signal_compliance"] == 0)
    )
    can_release = bool(
        (row["signal_compliance"] == 1)
        and (row["canary_delta"] <= cfg.canary_delta_limit)
        and (row["rollout_ring"] in {"ring_0", "ring_1", "ring_2"})
    )
    rollback_triggered = int(not can_release)
    return {
        "pred_block": should_block,
        "pred_escalate": should_escalate,
        "release_allowed": can_release,
        "rollback_triggered": rollback_triggered,
    }
"""),
        mk_markdown_cell("## 7) Training / Calibration"),
        mk_code_cell("""
# Calibration uses quantiles from the synthetic training data.
calibrated_block = float(work_df["risk_score"].quantile(0.78))
calibrated_escalate = float(work_df["risk_score"].quantile(0.62))

CONFIG = GuardrailConfig(
    guardrail_type=CONFIG.guardrail_type,
    block_threshold=calibrated_block,
    escalate_threshold=calibrated_escalate,
    canary_delta_limit=CONFIG.canary_delta_limit,
    max_rollout_ring=CONFIG.max_rollout_ring,
)

pred_rows = work_df.apply(
    lambda r: evaluate_guardrail(r, CONFIG),
    axis=1,
    result_type="expand",
)
scored_df = pd.concat([work_df, pred_rows], axis=1)
scored_df.head(5)
"""),
        mk_markdown_cell("## 8) Evaluation and Metrics"),
        mk_code_cell("""
def compute_metrics(df: pd.DataFrame) -> dict[str, float]:
    y_true = df["true_block"].to_numpy(dtype=np.int32)
    y_pred = df["pred_block"].to_numpy(dtype=np.int32)

    accuracy = float((y_true == y_pred).mean())
    tp = float(np.sum((y_true == 1) & (y_pred == 1)))
    fp = float(np.sum((y_true == 0) & (y_pred == 1)))
    fn = float(np.sum((y_true == 1) & (y_pred == 0)))

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1_score = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )

    metrics = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "escalation_rate": float(df["pred_escalate"].mean()),
        "compliance_success_rate": float(df["release_allowed"].mean()),
        "canary_regression_delta": float(df["canary_delta"].mean()),
        "rollback_frequency": float(df["rollback_triggered"].mean()),
    }
    return metrics


metrics = compute_metrics(scored_df)
metrics
"""),
        mk_code_cell("""
def benchmark_guardrail(
    df: pd.DataFrame,
    cfg: GuardrailConfig,
    runs: int = 25,
) -> dict[str, float]:
    samples_ms: list[float] = []
    for _ in range(runs):
        start = perf_counter()
        _ = df.apply(lambda r: evaluate_guardrail(r, cfg), axis=1)
        elapsed_ms = (perf_counter() - start) * 1000.0
        samples_ms.append(elapsed_ms)

    mean_ms = float(np.mean(samples_ms))
    p95_ms = float(np.percentile(samples_ms, 95))
    throughput = float((len(df) * runs) / (sum(samples_ms) / 1000.0))
    return {
        "benchmark_runs": float(runs),
        "mean_latency_ms": mean_ms,
        "p95_latency_ms": p95_ms,
        "throughput_rows_per_sec": throughput,
    }


benchmark = benchmark_guardrail(scored_df, CONFIG, runs=30)
benchmark
"""),
        mk_code_cell("""
# Basic regression checks to verify notebook behavior.
assert metrics["accuracy"] >= 0.65, "Accuracy below expected baseline"
assert metrics["precision"] >= 0.55, "Precision below expected baseline"
assert benchmark["p95_latency_ms"] < 400.0, "Latency regression detected"
assert benchmark["throughput_rows_per_sec"] > 300.0, "Throughput too low"
print("Validation checks passed.")
"""),
        mk_markdown_cell("## 9) Results Visualization"),
        mk_code_cell("""
plot_metrics = [
    "accuracy",
    "precision",
    "recall",
    "f1_score",
    "escalation_rate",
    "rollback_frequency",
]
plot_values = [metrics[key] for key in plot_metrics]

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(
    plot_metrics,
    plot_values,
    color=["#2f6db2", "#3f8e2f", "#ff9f1c", "#9d4edd", "#e76f51", "#264653"],
)
ax.set_ylim(0.0, 1.0)
ax.set_title(f"{CONFIG.guardrail_type} control metrics")
ax.set_ylabel("value")
ax.tick_params(axis="x", rotation=25)
plt.tight_layout()
plt.show()

latency = pd.DataFrame(
    {
        "mean_latency_ms": [benchmark["mean_latency_ms"]],
        "p95_latency_ms": [benchmark["p95_latency_ms"]],
        "throughput_rows_per_sec": [benchmark["throughput_rows_per_sec"]],
    }
)
latency
"""),
        mk_markdown_cell("## 10) Summary and Agent Workflow"),
        mk_markdown_cell("\n".join(summary_lines)),
    ]

    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.14.2",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main() -> None:
    readme_text = README.read_text(encoding="utf-8")
    agent_steps = parse_agent_workflow(readme_text)

    for md_path in sorted(BASE.glob("*-guardrails.md")):
        if md_path.name == "README.md":
            continue
        info = parse_sections(md_path.read_text(encoding="utf-8"))
        title = str(info["title"])
        scope = str(info["scope"])
        core_controls = (
            info["core_controls"] if isinstance(info["core_controls"], list) else []
        )
        validation_signals = (
            info["validation_signals"]
            if isinstance(info["validation_signals"], list)
            else []
        )
        use_cases = info["use_cases"] if isinstance(info["use_cases"], list) else []

        guardrail_slug = md_path.stem.replace("-guardrails", "").replace("-", "_")
        notebook = build_notebook(
            title=title,
            scope=scope,
            guardrail_slug=guardrail_slug,
            core_controls=core_controls,
            validation_signals=validation_signals,
            use_cases=use_cases,
            agent_steps=agent_steps,
        )

        nb_path = BASE / f"{md_path.stem}.ipynb"
        nb_path.write_text(json.dumps(notebook, indent=1), encoding="utf-8")
        print(f"updated {nb_path.as_posix()}")


if __name__ == "__main__":
    os.chdir(Path(__file__).resolve().parents[2])
    main()
