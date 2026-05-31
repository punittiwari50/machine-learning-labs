# Self-Attention Variants

This folder provides a structured guide to different self-attention variants from basic to advanced.

## Contents

- `basic.md`: Core self-attention variants and practical use cases.
- `advanced.md`: Advanced attention designs for long-context, efficiency, and enterprise-scale systems.
- `inference-performance-metrics/`: Inference serving metrics split into basic and advanced files.
- `basic.ipynb`: Runnable notebook implementing and comparing core self-attention variants.
- `advanced.ipynb`: Runnable notebook benchmarking advanced attention variants.
- `shared_text_preprocessing.py`: Shared tokenization and preprocessing helpers used by script variants.
- `basic_attention_numpy.py`: Same basic topic implemented with NumPy.
- `basic_attention_torch.py`: Same basic topic implemented with PyTorch.
- `basic_attention_tensorflow.py`: Same basic topic implemented with TensorFlow.
- `advanced_attention_numpy.py`: Advanced variant benchmarking script in NumPy.
- `advanced_attention_torch.py`: Advanced variant benchmarking script in PyTorch.
- `advanced_attention_tensorflow.py`: Advanced variant benchmarking script in TensorFlow.
- `run_attention_benchmarks.py`: Runs all basic and advanced scripts and prints a consolidated metrics table.
- `library-comparison.md`: Side-by-side run and output reference for all library variants.
- `guardrailing-engines/`: Guardrail types in separate notebooks and markdown files.

## Suggested Reading Order

1. Start with `basic.md`.
2. Run `basic.ipynb` for code-based implementation.
3. Move to `advanced.md`.
4. Run `advanced.ipynb` for advanced variant benchmarking.
5. Open `inference-performance-metrics/README.md` for the metrics-only track.
6. Open `guardrailing-engines/README.md` for the full guardrailing taxonomy and notebook track.

## Library-Specific Script Runs

Run from workspace root using WSL:

```bash
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; python self-attention-variants/basic_attention_numpy.py"
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; python self-attention-variants/basic_attention_torch.py"
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; python self-attention-variants/basic_attention_tensorflow.py"
```

## Automated Benchmarking Metrics

Both notebooks now export metrics automatically into separate JSON files by attention type, plus shared category files.

Basic notebook output directory:
- `self-attention-variants/outputs/basic-benchmarks/latest/`
- Per-type files:
	- `scaled_dot_product_metrics.json`
	- `multi_head_metrics.json`
	- `causal_metrics.json`
	- `local_window_metrics.json`
- Category files:
	- `latency_metrics.json`
	- `fidelity_metrics.json`
	- `summary_metrics.json`

Advanced notebook output directory:
- `self-attention-variants/outputs/advanced-benchmarks/latest/`
- Per-type files:
	- `dense_reference_metrics.json`
	- `sparse_metrics.json`
	- `linear_metrics.json`
	- `gqa_metrics.json`
- Category files:
	- `latency_metrics.json`
	- `fidelity_metrics.json`
	- `summary_metrics.json`
