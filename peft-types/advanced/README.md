# Advanced PEFT Matrix (Type-by-Type, Dual Framework)

This folder contains advanced PEFT examples implemented from scratch for all major PEFT types.

## TensorFlow
- tensorflow/01-lora-advanced-tensorflow.ipynb
- tensorflow/02-qlora-advanced-tensorflow.ipynb
- tensorflow/03-prefix-tuning-advanced-tensorflow.ipynb
- tensorflow/04-prompt-tuning-advanced-tensorflow.ipynb
- tensorflow/05-p-tuning-v2-advanced-tensorflow.ipynb
- tensorflow/06-ia3-advanced-tensorflow.ipynb
- tensorflow/07-adalora-advanced-tensorflow.ipynb
- tensorflow/08-bitfit-advanced-tensorflow.ipynb

## PyTorch
- pytorch/01-lora-advanced-pytorch.ipynb
- pytorch/02-qlora-advanced-pytorch.ipynb
- pytorch/03-prefix-tuning-advanced-pytorch.ipynb
- pytorch/04-prompt-tuning-advanced-pytorch.ipynb
- pytorch/05-p-tuning-v2-advanced-pytorch.ipynb
- pytorch/06-ia3-advanced-pytorch.ipynb
- pytorch/07-adalora-advanced-pytorch.ipynb
- pytorch/08-bitfit-advanced-pytorch.ipynb

Runtime device switch:
- Controlled by configs/runtime.env
- USE_GPU=1 (default) for GPU-first
- USE_GPU=0 to force CPU