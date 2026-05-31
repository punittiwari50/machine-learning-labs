# Self-Attention Variants - Library Comparison

This document compares the same topic implementation across three libraries using the same shared tokenization and preprocessing flow.

## Implementations

- NumPy: `basic_attention_numpy.py`
- PyTorch: `basic_attention_torch.py`
- TensorFlow: `basic_attention_tensorflow.py`
- Shared preprocessing: `shared_text_preprocessing.py`

## Advanced Script Variants

- NumPy advanced script: `advanced_attention_numpy.py`
- PyTorch advanced script: `advanced_attention_torch.py`
- TensorFlow advanced script: `advanced_attention_tensorflow.py`

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
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; python self-attention-variants/basic_attention_numpy.py"
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; python self-attention-variants/basic_attention_torch.py"
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; python self-attention-variants/basic_attention_tensorflow.py"
```

Consolidated run across all basic+advanced scripts:

```bash
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; python self-attention-variants/run_attention_benchmarks.py"
```

## Last Verified Outputs

- NumPy: `{'library': 'numpy', 'accuracy': 0.5}`
- PyTorch: `{'library': 'pytorch', 'device': 'cuda', 'accuracy': 0.5}`
- TensorFlow: `{'library': 'tensorflow', 'runtime_device': 'cuda', 'accuracy': 0.5}`

## Notes

- All variants use the same text-first preprocessing contract to avoid train/serve skew.
- PyTorch variant includes a detached feature stage before training the classifier head to avoid autograd graph reuse issues.
- Runtime device selection in PyTorch and TensorFlow respects `USE_GPU`.
