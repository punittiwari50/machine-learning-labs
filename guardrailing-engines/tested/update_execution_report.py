from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPORT_PATH = ROOT / "execution-report.md"
SNAPSHOT_PATH = ROOT / "benchmark-snapshot.json"

TARGET_NOTEBOOKS = [
    "input-guardrails_tested.ipynb",
    "retrieval-guardrails_tested.ipynb",
    "generation-guardrails_tested.ipynb",
    "tool-action-guardrails_tested.ipynb",
    "post-generation-delivery-guardrails_tested.ipynb",
    "runtime-infrastructure-guardrails_tested.ipynb",
    "human-in-the-loop-guardrails_tested.ipynb",
]

P95_THRESHOLD_MS = 450.0
THROUGHPUT_THRESHOLD = 250.0


@dataclass(frozen=True)
class BenchmarkRow:
    notebook: str
    mean_latency_ms: float
    p95_latency_ms: float
    throughput_rows_per_sec: float
    assertions_passed: bool


def _load_notebook(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _assertions_passed(cells: list[dict[str, object]]) -> bool:
    for cell in cells:
        if cell.get("cell_type") != "code":
            continue
        outputs = cell.get("outputs", [])
        if not isinstance(outputs, list):
            continue
        for output in outputs:
            if isinstance(output, dict) and output.get("output_type") == "error":
                return False
    return True


def _extract_benchmark_dict(cells: list[dict[str, object]]) -> dict[str, float] | None:
    pattern = re.compile(
        r"\{[^{}]*'mean_latency_ms'\s*:\s*[-+0-9.eE]+[^{}]*"
        r"'p95_latency_ms'\s*:\s*[-+0-9.eE]+[^{}]*"
        r"'throughput_rows_per_sec'\s*:\s*[-+0-9.eE]+[^{}]*\}"
    )

    for cell in cells:
        if cell.get("cell_type") != "code":
            continue
        outputs = cell.get("outputs", [])
        if not isinstance(outputs, list):
            continue
        for output in outputs:
            if not isinstance(output, dict):
                continue
            data = output.get("data", {})
            if not isinstance(data, dict):
                continue
            text_plain = data.get("text/plain", [])
            if isinstance(text_plain, str):
                text = text_plain
            elif isinstance(text_plain, list):
                text = "".join(str(part) for part in text_plain)
            else:
                text = ""

            match = pattern.search(text)
            if match:
                payload = ast.literal_eval(match.group(0))
                return {
                    "mean_latency_ms": float(payload["mean_latency_ms"]),
                    "p95_latency_ms": float(payload["p95_latency_ms"]),
                    "throughput_rows_per_sec": float(
                        payload["throughput_rows_per_sec"]
                    ),
                }
    return None


def _extract_current_rows() -> list[BenchmarkRow]:
    rows: list[BenchmarkRow] = []
    for notebook_name in TARGET_NOTEBOOKS:
        path = ROOT / notebook_name
        if not path.exists():
            raise SystemExit(f"Missing tested notebook: {notebook_name}")

        notebook = _load_notebook(path)
        cells = notebook.get("cells", [])
        if not isinstance(cells, list):
            raise SystemExit(f"Invalid notebook format: {notebook_name}")

        benchmark = _extract_benchmark_dict(
            [cell for cell in cells if isinstance(cell, dict)]
        )
        if benchmark is None:
            raise SystemExit(f"Benchmark metrics not found in outputs: {notebook_name}")

        rows.append(
            BenchmarkRow(
                notebook=notebook_name,
                mean_latency_ms=benchmark["mean_latency_ms"],
                p95_latency_ms=benchmark["p95_latency_ms"],
                throughput_rows_per_sec=benchmark["throughput_rows_per_sec"],
                assertions_passed=_assertions_passed(
                    [cell for cell in cells if isinstance(cell, dict)]
                ),
            )
        )
    return rows


def _load_previous_metrics() -> dict[str, dict[str, float]]:
    if SNAPSHOT_PATH.exists():
        data = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
        metrics = data.get("metrics", {})
        if isinstance(metrics, dict):
            return {
                str(k): {
                    "mean_latency_ms": float(v["mean_latency_ms"]),
                    "throughput_rows_per_sec": float(v["throughput_rows_per_sec"]),
                }
                for k, v in metrics.items()
                if isinstance(v, dict)
                and "mean_latency_ms" in v
                and "throughput_rows_per_sec" in v
            }

    if not REPORT_PATH.exists():
        return {}

    previous: dict[str, dict[str, float]] = {}
    row_pattern = re.compile(
        r"^\|\s*([^|]+?)\s*\|\s*([-+0-9.]+)\s*\|\s*([-+0-9.]+)\s*\|\s*([-+0-9.]+)\s*\|"
    )
    for line in REPORT_PATH.read_text(encoding="utf-8").splitlines():
        match = row_pattern.match(line.strip())
        if not match:
            continue
        notebook = match.group(1).strip()
        if notebook not in TARGET_NOTEBOOKS:
            continue
        previous[notebook] = {
            "mean_latency_ms": float(match.group(2)),
            "throughput_rows_per_sec": float(match.group(4)),
        }
    return previous


def _fmt_delta_ms(delta: float | None) -> str:
    if delta is None:
        return "baseline"
    return f"{delta:+.4f} ms"


def _fmt_delta_tps(delta: float | None) -> str:
    if delta is None:
        return "baseline"
    return f"{delta:+.4f} rows/s"


def _build_report(
    rows: list[BenchmarkRow], previous: dict[str, dict[str, float]]
) -> str:
    lines = [
        "# Guardrailing Engines Benchmark Dashboard",
        "",
        f"**Date**: {date.today().isoformat()}",
        (
            "**Scope**: Consolidated benchmark and verification dashboard"
            " for guardrail notebooks."
        ),
        "",
        "## Validation Method",
        (
            "- Source of metrics: executed outputs in tested notebooks under"
            " guardrailing-engines/tested."
        ),
        "- Benchmarks tracked per notebook:",
        "  - mean_latency_ms",
        "  - p95_latency_ms",
        "  - throughput_rows_per_sec",
        "- Quality gate inference:",
        (
            "  - assertions_passed = true when no AssertionError or traceback"
            " appears in notebook outputs."
        ),
        "",
        "## Threshold Policy",
        f"- P95 latency threshold: < {P95_THRESHOLD_MS:.1f} ms",
        f"- Throughput threshold: > {THROUGHPUT_THRESHOLD:.1f} rows/s",
        "",
        "## Consolidated Benchmark Table",
        "",
        (
            "| Notebook | Mean Latency (ms) | P95 Latency (ms) |"
            " Throughput (rows/s) | P95 Threshold | Throughput Threshold |"
            " Threshold Status | Trend Mean Latency | Trend Throughput |"
            " Assertions |"
        ),
        "|---|---:|---:|---:|---:|---:|---|---|---|---|",
    ]

    for row in rows:
        prev = previous.get(row.notebook)
        mean_delta = (
            None if prev is None else row.mean_latency_ms - prev["mean_latency_ms"]
        )
        throughput_delta = (
            None
            if prev is None
            else row.throughput_rows_per_sec - prev["throughput_rows_per_sec"]
        )
        threshold_ok = (
            row.p95_latency_ms < P95_THRESHOLD_MS
            and row.throughput_rows_per_sec > THROUGHPUT_THRESHOLD
        )
        lines.append(
            "| "
            f"{row.notebook} | "
            f"{row.mean_latency_ms:.4f} | "
            f"{row.p95_latency_ms:.4f} | "
            f"{row.throughput_rows_per_sec:.4f} | "
            f"< {P95_THRESHOLD_MS:.1f} | "
            f"> {THROUGHPUT_THRESHOLD:.1f} | "
            f"{'PASS' if threshold_ok else 'FAIL'} | "
            f"{_fmt_delta_ms(mean_delta)} | "
            f"{_fmt_delta_tps(throughput_delta)} | "
            f"{'PASS' if row.assertions_passed else 'FAIL'} |"
        )

    lines.extend(
        [
            "",
            "## Notes",
            (
                "- Trend columns are automatically computed against the prior"
                " snapshot/report values."
            ),
            (
                "- Snapshot is updated after each report generation at"
                " guardrailing-engines/tested/"
                "benchmark-snapshot.json."
            ),
        ]
    )
    return "\n".join(lines) + "\n"


def _write_snapshot(rows: list[BenchmarkRow]) -> None:
    payload = {
        "generated_at": date.today().isoformat(),
        "metrics": {
            row.notebook: {
                "mean_latency_ms": row.mean_latency_ms,
                "p95_latency_ms": row.p95_latency_ms,
                "throughput_rows_per_sec": row.throughput_rows_per_sec,
                "assertions_passed": row.assertions_passed,
            }
            for row in rows
        },
    }
    SNAPSHOT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    rows = _extract_current_rows()
    previous = _load_previous_metrics()
    report_text = _build_report(rows, previous)
    REPORT_PATH.write_text(report_text, encoding="utf-8")
    _write_snapshot(rows)
    print("UPDATED_EXECUTION_REPORT_WITH_DELTAS")


if __name__ == "__main__":
    main()
