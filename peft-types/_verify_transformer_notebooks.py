from __future__ import annotations

from pathlib import Path
import subprocess
import time


def main() -> int:
    root = Path("/mnt/c/DEV/PROJECTS/ML_BASICS/machine-learning-labs/peft-types")
    notebooks: list[Path] = []
    for rel in [
        "transformer-basic/tensorflow",
        "transformer-basic/pytorch",
        "transformer-advance/tensorflow",
        "transformer-advance/pytorch",
    ]:
        notebooks.extend(sorted((root / rel).glob("*.ipynb")))

    print(f"total_notebooks={len(notebooks)}")

    results: list[tuple[str, int, float, str]] = []
    start_all = time.time()

    for nb in notebooks:
        out = Path("/tmp") / f"{nb.stem}_full_tested.ipynb"
        t0 = time.time()
        proc = subprocess.run(
            [
                "jupyter",
                "nbconvert",
                "--to",
                "notebook",
                "--execute",
                str(nb),
                "--output",
                str(out),
            ],
            capture_output=True,
            text=True,
        )
        dt = time.time() - t0
        tail_src = (proc.stderr or proc.stdout or "").splitlines()
        tail = "\n".join(tail_src[-12:])
        results.append((nb.name, proc.returncode, dt, tail))
        print(f"{nb.name} returncode={proc.returncode} duration_sec={dt:.1f}")

    passed = [r for r in results if r[1] == 0]
    failed = [r for r in results if r[1] != 0]
    elapsed = time.time() - start_all
    print(f"passed={len(passed)} failed={len(failed)} elapsed_sec={elapsed:.1f}")

    if failed:
        print("\nFAILED_NOTEBOOKS:")
        for name, rc, dt, tail in failed:
            print(f"--- {name} rc={rc} duration_sec={dt:.1f}")
            print(tail)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
