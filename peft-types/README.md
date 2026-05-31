# PEFT Types - Notebook Collection

This folder contains PEFT notebooks organized as folder-based matrices. Each notebook follows a full flow:
imports -> config -> data -> EDA -> preprocessing -> model -> training -> evaluation -> visualization -> summary.

Small project used in all notebooks:
Support-ticket urgency classification (labels: low, medium, high).

Top-level legacy PEFT notebooks were removed after matrix consolidation.

Basic cross-framework PEFT matrix (all types):
- basic/tensorflow/01-lora-basic-tensorflow.ipynb
- basic/tensorflow/02-qlora-basic-tensorflow.ipynb
- basic/tensorflow/03-prefix-tuning-basic-tensorflow.ipynb
- basic/tensorflow/04-prompt-tuning-basic-tensorflow.ipynb
- basic/tensorflow/05-p-tuning-v2-basic-tensorflow.ipynb
- basic/tensorflow/06-ia3-basic-tensorflow.ipynb
- basic/tensorflow/07-adalora-basic-tensorflow.ipynb
- basic/tensorflow/08-bitfit-basic-tensorflow.ipynb
- basic/pytorch/01-lora-basic-pytorch.ipynb
- basic/pytorch/02-qlora-basic-pytorch.ipynb
- basic/pytorch/03-prefix-tuning-basic-pytorch.ipynb
- basic/pytorch/04-prompt-tuning-basic-pytorch.ipynb
- basic/pytorch/05-p-tuning-v2-basic-pytorch.ipynb
- basic/pytorch/06-ia3-basic-pytorch.ipynb
- basic/pytorch/07-adalora-basic-pytorch.ipynb
- basic/pytorch/08-bitfit-basic-pytorch.ipynb
- See basic/README.md for the full basic matrix and shared logic structure.

Advanced matrix (all types, separate folder):
- advanced/tensorflow/01-lora-advanced-tensorflow.ipynb
- advanced/tensorflow/02-qlora-advanced-tensorflow.ipynb
- advanced/tensorflow/03-prefix-tuning-advanced-tensorflow.ipynb
- advanced/tensorflow/04-prompt-tuning-advanced-tensorflow.ipynb
- advanced/tensorflow/05-p-tuning-v2-advanced-tensorflow.ipynb
- advanced/tensorflow/06-ia3-advanced-tensorflow.ipynb
- advanced/tensorflow/07-adalora-advanced-tensorflow.ipynb
- advanced/tensorflow/08-bitfit-advanced-tensorflow.ipynb
- advanced/pytorch/01-lora-advanced-pytorch.ipynb
- advanced/pytorch/02-qlora-advanced-pytorch.ipynb
- advanced/pytorch/03-prefix-tuning-advanced-pytorch.ipynb
- advanced/pytorch/04-prompt-tuning-advanced-pytorch.ipynb
- advanced/pytorch/05-p-tuning-v2-advanced-pytorch.ipynb
- advanced/pytorch/06-ia3-advanced-pytorch.ipynb
- advanced/pytorch/07-adalora-advanced-pytorch.ipynb
- advanced/pytorch/08-bitfit-advanced-pytorch.ipynb
- See advanced/README.md for the full matrix.

Transformer basic matrix (all types, separate folder):
- transformer-basic/tensorflow/01-lora-transformer-basic-tensorflow.ipynb
- transformer-basic/tensorflow/02-qlora-transformer-basic-tensorflow.ipynb
- transformer-basic/tensorflow/03-prefix-tuning-transformer-basic-tensorflow.ipynb
- transformer-basic/tensorflow/04-prompt-tuning-transformer-basic-tensorflow.ipynb
- transformer-basic/tensorflow/05-p-tuning-v2-transformer-basic-tensorflow.ipynb
- transformer-basic/tensorflow/06-ia3-transformer-basic-tensorflow.ipynb
- transformer-basic/tensorflow/07-adalora-transformer-basic-tensorflow.ipynb
- transformer-basic/tensorflow/08-bitfit-transformer-basic-tensorflow.ipynb
- transformer-basic/pytorch/01-lora-transformer-basic-pytorch.ipynb
- transformer-basic/pytorch/02-qlora-transformer-basic-pytorch.ipynb
- transformer-basic/pytorch/03-prefix-tuning-transformer-basic-pytorch.ipynb
- transformer-basic/pytorch/04-prompt-tuning-transformer-basic-pytorch.ipynb
- transformer-basic/pytorch/05-p-tuning-v2-transformer-basic-pytorch.ipynb
- transformer-basic/pytorch/06-ia3-transformer-basic-pytorch.ipynb
- transformer-basic/pytorch/07-adalora-transformer-basic-pytorch.ipynb
- transformer-basic/pytorch/08-bitfit-transformer-basic-pytorch.ipynb
- See transformer-basic/README.md for the full matrix.

Transformer advanced matrix (all types, separate folder):
- transformer-advance/tensorflow/01-lora-transformer-advance-tensorflow.ipynb
- transformer-advance/tensorflow/02-qlora-transformer-advance-tensorflow.ipynb
- transformer-advance/tensorflow/03-prefix-tuning-transformer-advance-tensorflow.ipynb
- transformer-advance/tensorflow/04-prompt-tuning-transformer-advance-tensorflow.ipynb
- transformer-advance/tensorflow/05-p-tuning-v2-transformer-advance-tensorflow.ipynb
- transformer-advance/tensorflow/06-ia3-transformer-advance-tensorflow.ipynb
- transformer-advance/tensorflow/07-adalora-transformer-advance-tensorflow.ipynb
- transformer-advance/tensorflow/08-bitfit-transformer-advance-tensorflow.ipynb
- transformer-advance/pytorch/01-lora-transformer-advance-pytorch.ipynb
- transformer-advance/pytorch/02-qlora-transformer-advance-pytorch.ipynb
- transformer-advance/pytorch/03-prefix-tuning-transformer-advance-pytorch.ipynb
- transformer-advance/pytorch/04-prompt-tuning-transformer-advance-pytorch.ipynb
- transformer-advance/pytorch/05-p-tuning-v2-transformer-advance-pytorch.ipynb
- transformer-advance/pytorch/06-ia3-transformer-advance-pytorch.ipynb
- transformer-advance/pytorch/07-adalora-transformer-advance-pytorch.ipynb
- transformer-advance/pytorch/08-bitfit-transformer-advance-pytorch.ipynb
- See transformer-advance/README.md for the full matrix.

Advanced coverage note:
- The advanced section includes all PEFT types through direct implementation and explicit advanced concept mapping.
- See advanced/README.md for the full coverage matrix and where each type is implemented in detail.

Runtime device policy:
- Default mode is GPU-first.
- Set `USE_GPU=1` in `configs/runtime.env` to use GPU when available.
- Set `USE_GPU=0` in `configs/runtime.env` to force CPU.
- Restart and run each notebook from the first code cell after changing this value.
