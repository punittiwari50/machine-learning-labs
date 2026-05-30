---
description: "Use when writing or reviewing Python, ML pipeline, or system code for performance. Covers profiling, memory efficiency, vectorization, caching, lazy evaluation, and ML-specific throughput optimization."
applyTo: ["**/*.py", "**/*.ipynb"]
---

# Performance Standards

## Core Principle

**Measure first, optimize second.** Never optimize without a profiled bottleneck. Every optimization must have a before/after benchmark.

---

## Tier 1 — Algorithmic Performance (Always Apply)

- Choose the correct data structure for the access pattern:
  - O(1) lookup → `dict` / `set` over `list`
  - Sorted search → `bisect` over linear scan
  - Priority access → `heapq`
- Avoid nested loops over large datasets; use vectorized NumPy/Pandas operations instead.
- Use generators and iterators for large sequences; never materialize a full list when streaming suffices.

```python
# Bad — materializes entire list
results = [expensive(x) for x in million_items]

# Good — lazy generator
results = (expensive(x) for x in million_items)
```

---

## Tier 2 — Python Runtime Performance

### Vectorization Over Loops

```python
# Bad
for i in range(len(arr)):
    arr[i] = arr[i] * 2

# Good
arr = arr * 2  # NumPy ufunc, ~100x faster
```

### Avoid Repeated Attribute Lookups

```python
# Bad — resolves np.sqrt on every iteration
for x in data:
    result = np.sqrt(x)

# Good
sqrt = np.sqrt
for x in data:
    result = sqrt(x)
```

### String Building

```python
# Bad — O(n²) memory
s = ""
for part in parts:
    s += part

# Good — O(n)
s = "".join(parts)
```

---

## Tier 3 — Memory Management

- Use `np.float32` instead of `float64` for ML tensors unless precision demands otherwise — halves memory.
- Delete large intermediate variables explicitly: `del X_intermediate; gc.collect()`.
- Use `tf.data.Dataset` pipelines with `.prefetch()` and `.cache()` — never load entire datasets into RAM.
- Prefer in-place operations for large arrays when the original is not needed.

```python
# Memory-efficient TF data pipeline
dataset = (
    tf.data.Dataset.from_tensor_slices((X, y))
    .shuffle(buffer_size=1024)
    .batch(BATCH_SIZE)
    .cache()
    .prefetch(tf.data.AUTOTUNE)
)
```

---

## Tier 4 — Caching & Memoization

- Cache expensive pure-function results with `functools.lru_cache` or `functools.cache`.
- Cache preprocessed datasets to disk (pickle, `.npy`, TFRecord) — never recompute in every run.
- Use `joblib.Memory` for caching sklearn-style transformers.

```python
from functools import lru_cache

@lru_cache(maxsize=512)
def encode_token(token: str) -> int:
    return vocabulary[token]
```

---

## Tier 5 — ML Pipeline Throughput

| Bottleneck | Fix |
|-----------|-----|
| CPU-bound preprocessing | `tf.data` with `num_parallel_calls=tf.data.AUTOTUNE` |
| GPU under-utilization | Increase batch size; use mixed precision (`tf.keras.mixed_precision`) |
| Slow tokenization | Pre-tokenize and cache to TFRecord |
| Repeated model reloads | Load once, call many times |
| Unoptimized inference | Use `model.predict()` over `model(x)` in loops; use TF SavedModel |

### Mixed Precision (GPU Training)

```python
from tensorflow.keras import mixed_precision
mixed_precision.set_global_policy("mixed_float16")
```

---

## Tier 6 — Profiling Workflow (Required Before Reporting Performance Claims)

```python
# CPU profiling
import cProfile
cProfile.run("train_model(X, y)", sort="cumulative")

# Line-level profiling (install line_profiler)
# %lprun -f train_step train_model(X, y)

# Memory profiling
from memory_profiler import memory_usage
mem = memory_usage((train_model, (X, y)), interval=0.1)
print(f"Peak memory: {max(mem):.1f} MiB")
```

Benchmark template:

```python
import time
from typing import Callable, Any

def benchmark(fn: Callable, *args: Any, runs: int = 5) -> float:
    """Return mean execution time in milliseconds over `runs` iterations."""
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        fn(*args)
        times.append((time.perf_counter() - start) * 1000)
    mean_ms = sum(times) / len(times)
    print(f"{fn.__name__}: {mean_ms:.2f} ms (n={runs})")
    return mean_ms
```

---

## Quality Gates

- [ ] No O(n²) loops over datasets with > 1 000 rows.
- [ ] No full dataset materialised when a generator/pipeline suffices.
- [ ] Mixed precision enabled for GPU training notebooks.
- [ ] At least one benchmark cell present in any notebook making performance claims.
