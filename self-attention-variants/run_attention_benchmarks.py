from __future__ import annotations

import ast
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ScriptSpec:
    label: str
    script_name: str


SCRIPTS: tuple[ScriptSpec, ...] = (
    ScriptSpec("basic-numpy", "basic_attention_numpy.py"),
    ScriptSpec("basic-torch", "basic_attention_torch.py"),
    ScriptSpec("basic-tensorflow", "basic_attention_tensorflow.py"),
    ScriptSpec("advanced-numpy", "advanced_attention_numpy.py"),
    ScriptSpec("advanced-torch", "advanced_attention_torch.py"),
    ScriptSpec("advanced-tensorflow", "advanced_attention_tensorflow.py"),
)


def parse_metrics(stdout: str) -> dict[str, object]:
    lines = [line.strip() for line in stdout.splitlines() if line.strip()]
    if not lines:
        raise ValueError("Script produced no stdout to parse.")
    return ast.literal_eval(lines[-1])


def run_script(script_path: Path) -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, str(script_path)],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"{script_path.name} failed with exit code {completed.returncode}\n"
            f"STDOUT:\n{completed.stdout}\n"
            f"STDERR:\n{completed.stderr}"
        )
    return parse_metrics(completed.stdout)


def metric_value(metrics: dict[str, object], key: str) -> str:
    value = metrics.get(key)
    if isinstance(value, float):
        return f"{value:.6f}"
    if value is None:
        return "-"
    return str(value)


def print_table(rows: list[dict[str, object]]) -> None:
    headers = [
        "label",
        "library",
        "variant",
        "runtime",
        "accuracy",
        "best_temp",
        "dense_ms",
        "sparse_ms",
        "linear_ms",
        "gqa_ms",
        "sparse_mse",
        "linear_mse",
        "gqa_mse",
    ]

    table_rows: list[list[str]] = []
    for row in rows:
        runtime = str(row.get("device") or row.get("runtime_device") or "-")
        table_rows.append(
            [
                str(row.get("label", "-")),
                str(row.get("library", "-")),
                str(row.get("variant", "-")),
                runtime,
                metric_value(row, "accuracy"),
                metric_value(row, "best_temperature"),
                metric_value(row, "dense_ms"),
                metric_value(row, "sparse_ms"),
                metric_value(row, "linear_ms"),
                metric_value(row, "gqa_ms"),
                metric_value(row, "sparse_mse_vs_dense"),
                metric_value(row, "linear_mse_vs_dense"),
                metric_value(row, "gqa_mse_vs_dense"),
            ]
        )

    widths = [len(h) for h in headers]
    for table_row in table_rows:
        for i, value in enumerate(table_row):
            widths[i] = max(widths[i], len(value))

    def format_row(values: list[str]) -> str:
        return " | ".join(value.ljust(widths[i]) for i, value in enumerate(values))

    print(format_row(headers))
    print("-+-".join("-" * w for w in widths))
    for table_row in table_rows:
        print(format_row(table_row))


def main() -> None:
    root = Path(__file__).resolve().parent
    results: list[dict[str, object]] = []

    for spec in SCRIPTS:
        script_path = root / spec.script_name
        metrics = run_script(script_path)
        metrics["label"] = spec.label
        results.append(metrics)

    print_table(results)


if __name__ == "__main__":
    main()
