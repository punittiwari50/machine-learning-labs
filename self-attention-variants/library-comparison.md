# Self-Attention Variants - Library Comparison

This document compares the same topic implementation across three libraries using the same shared tokenization and preprocessing flow.

## Implementations

- NumPy: `scripts/basic_attention_numpy.py`
- PyTorch: `scripts/basic_attention_torch.py`
- TensorFlow: `scripts/basic_attention_tensorflow.py`
- Shared preprocessing: `scripts/shared_text_preprocessing.py`

## Advanced Script Variants

- NumPy advanced script: `scripts/advanced_attention_numpy.py`
- PyTorch advanced script: `scripts/advanced_attention_torch.py`
- TensorFlow advanced script: `scripts/advanced_attention_tensorflow.py`

## Notebook Variants

- NumPy notebook: `basic_attention_numpy.ipynb`
- PyTorch notebook: `basic_attention_torch.ipynb`
- TensorFlow notebook: `basic_attention_tensorflow.ipynb`

## Advanced Notebook Variants

- NumPy advanced notebook: `advanced_attention_numpy.ipynb`
- PyTorch advanced notebook: `advanced_attention_torch.ipynb`
- TensorFlow advanced notebook: `advanced_attention_tensorflow.ipynb`

## Execution Commands (WSL)

```bash
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; python self-attention-variants/scripts/basic_attention_numpy.py"
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; python self-attention-variants/scripts/basic_attention_torch.py"
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; python self-attention-variants/scripts/basic_attention_tensorflow.py"
```

Run all variants with one command:

```bash
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; python self-attention-variants/scripts/run_attention_benchmarks.py"
```

Consolidated run across all basic+advanced scripts:

```bash
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; python self-attention-variants/scripts/run_attention_benchmarks.py"
```

## Last Verified Outputs

- NumPy: `{'library': 'numpy', 'accuracy': 0.5}`
- PyTorch: `{'library': 'pytorch', 'device': 'cuda', 'accuracy': 0.5}`
- TensorFlow: `{'library': 'tensorflow', 'runtime_device': 'cuda', 'accuracy': 0.5}`

## Notes

- All variants use the same text-first preprocessing contract to avoid train/serve skew.
- PyTorch variant includes a detached feature stage before training the classifier head to avoid autograd graph reuse issues.
- Runtime device selection in PyTorch and TensorFlow respects `USE_GPU`.

## Consolidated Snapshot (2026-06-01)

Source: `python self-attention-variants/scripts/run_attention_benchmarks.py`

| label | library | variant | runtime | accuracy | best_temp | dense_ms | sparse_ms | linear_ms | gqa_ms | sparse_mse | linear_mse | gqa_mse |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| basic-numpy | numpy | - | - | 0.500000 | - | - | - | - | - | - | - | - |
| basic-torch | pytorch | - | cuda | 0.500000 | - | - | - | - | - | - | - | - |
| basic-tensorflow | tensorflow | - | cuda | 0.576923 | - | - | - | - | - | - | - | - |
| advanced-numpy | numpy | advanced | - | - | 2.000000 | 0.999062 | 1.013902 | 3.127575 | 2.656416 | 0.001421 | 0.000086 | 0.023211 |
| advanced-torch | pytorch | advanced | cuda | - | 2.000000 | 1.229437 | 2.299265 | 99.454782 | 13.687842 | 0.002035 | 0.000241 | 0.030836 |
| advanced-tensorflow | tensorflow | advanced | cuda | - | 2.000000 | 0.477347 | 1.049525 | 84.813750 | 23.065867 | 0.002156 | 0.000020 | 0.042706 |
