from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOTEBOOKS = sorted(ROOT.glob("*_tested.ipynb"))


def has_error_output(cell: dict[str, object]) -> bool:
    outputs = cell.get("outputs", [])
    if not isinstance(outputs, list):
        return False
    for output in outputs:
        if isinstance(output, dict) and output.get("output_type") == "error":
            return True
    return False


def main() -> None:
    if not NOTEBOOKS:
        raise SystemExit("No tested notebooks found.")

    for notebook_path in NOTEBOOKS:
        data = json.loads(notebook_path.read_text(encoding="utf-8"))
        cells = data.get("cells", [])
        if not isinstance(cells, list):
            raise SystemExit(f"Invalid notebook format: {notebook_path.name}")

        code_cells = [
            cell
            for cell in cells
            if isinstance(cell, dict) and cell.get("cell_type") == "code"
        ]
        error_cells = [cell for cell in code_cells if has_error_output(cell)]
        output_cells = [
            cell
            for cell in code_cells
            if isinstance(cell.get("outputs"), list) and cell.get("outputs")
        ]

        print(
            json.dumps(
                {
                    "notebook": notebook_path.name,
                    "code_cells": len(code_cells),
                    "cells_with_outputs": len(output_cells),
                    "error_cells": len(error_cells),
                },
                indent=2,
            )
        )

        if error_cells:
            raise SystemExit(f"Notebook has error output: {notebook_path.name}")
        if not output_cells:
            raise SystemExit(f"Notebook has no outputs: {notebook_path.name}")

    print("ALL_TESTED_NOTEBOOKS_VALID")


if __name__ == "__main__":
    main()
