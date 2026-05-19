# Overview & Setup

# Types of Machine Learning Embeddings (TensorFlow, OpenCV, TensorFlow Text)

This notebook provides a practical taxonomy of embedding types with:
- Concepts and subtypes
- Purpose for each subtype
- Code examples with comments
- Do and Don't checklists
- Tips and tricks
- Summary and application use cases

## Scope
Focused on workflows built with **TensorFlow**, **tensorflow-text**, and **OpenCV**.

---

## 0) Setup

---

```python
# Core imports
import os
import numpy as np
import tensorflow as tf

# Optional imports for this notebook
try:
    import tensorflow_text as tf_text
    TF_TEXT_AVAILABLE = True
except Exception:
    TF_TEXT_AVAILABLE = False

try:
    import cv2
    OPENCV_AVAILABLE = True
except Exception:
    OPENCV_AVAILABLE = False

print('TensorFlow:', tf.__version__)
print('tensorflow-text available:', TF_TEXT_AVAILABLE)
print('OpenCV available:', OPENCV_AVAILABLE)
```

---

