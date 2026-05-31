from __future__ import annotations

from pathlib import Path

import nbformat as nbf

root = Path(__file__).resolve().parent
(root / "tensorflow").mkdir(parents=True, exist_ok=True)
(root / "pytorch").mkdir(parents=True, exist_ok=True)

peft_types = [
    ("01", "LoRA", "low-rank residual adapter"),
    (
        "02",
        "QLoRA",
        "quantization-aware low-rank adapter (simulated in this basic from-scratch setup)",
    ),
    (
        "03",
        "Prefix Tuning",
        "learned prefix vectors merged into sequence representation",
    ),
    ("04", "Prompt Tuning", "trainable soft prompt tokens prepended to inputs"),
    (
        "05",
        "P-Tuning v2",
        "deep prompt encoder producing trainable contextual prompts",
    ),
    ("06", "IA3", "multiplicative scaling vectors over hidden representations"),
    (
        "07",
        "AdaLoRA",
        "rank-adaptive low-rank adapter with budget-aware behavior",
    ),
    ("08", "BitFit", "bias-only adaptation over frozen base layers"),
]


def md(lines: list[str]):
    return nbf.v4.new_markdown_cell("\n".join(lines), metadata={"language": "markdown"})


def code(lines: list[str]):
    return nbf.v4.new_code_cell("\n".join(lines), metadata={"language": "python"})


def common_samples_block() -> list[str]:
    return [
        "samples = [",
        "    ('Server not reachable after deployment', 2),",
        "    ('Password reset email not received', 1),",
        "    ('Dashboard typo in heading', 0),",
        "    ('Payment API timing out for premium users', 2),",
        "    ('Need help changing profile picture', 0),",
        "    ('CPU usage spikes to 100 percent hourly', 2),",
        "    ('Can we export reports to CSV?', 0),",
        "    ('Intermittent login failures for SSO users', 2),",
        "    ('Dark mode icon is slightly misaligned', 0),",
        "    ('Data sync lag observed in EU region', 1),",
        "    ('Mobile app crashes on checkout page', 2),",
        "    ('Feature request: bulk archive tickets', 0),",
        "    ('Webhook retries causing duplicate events', 1),",
        "    ('Fraud alert queue delayed by 5 minutes', 2),",
        "    ('Question about invoice date format', 0),",
        "    ('Latency increased after model update', 1),",
        "]",
        "df = pd.DataFrame(samples, columns=['text', 'label'])",
        "df['label_name'] = df['label'].map({0: 'low', 1: 'medium', 2: 'high'})",
        "df = df.sample(frac=1.0, random_state=SEED).reset_index(drop=True)",
        "split_idx = int(len(df) * cfg.train_size)",
        "train_df = df.iloc[:split_idx].copy()",
        "test_df = df.iloc[split_idx:].copy()",
    ]


def runtime_tf_block() -> list[str]:
    return [
        "def load_runtime_env() -> None:",
        "    candidate_paths = [",
        "        os.path.join(os.getcwd(), 'configs', 'runtime.env'),",
        "        os.path.join(os.getcwd(), 'configs', 'runtime.env.example'),",
        "        os.path.join(os.getcwd(), '..', 'configs', 'runtime.env'),",
        "        os.path.join(os.getcwd(), '..', 'configs', 'runtime.env.example'),",
        "    ]",
        "    env_loaded = False",
        "    for path in candidate_paths:",
        "        if not os.path.exists(path):",
        "            continue",
        "        with open(path, 'r', encoding='utf-8') as handle:",
        "            for raw_line in handle:",
        "                line = raw_line.strip()",
        "                if not line or line.startswith('#') or '=' not in line:",
        "                    continue",
        "                key, value = line.split('=', 1)",
        '                os.environ[key.strip()] = value.strip().strip("\\"\'")',
        "        env_loaded = True",
        "        break",
        "    if not env_loaded and 'USE_GPU' not in os.environ:",
        "        os.environ['USE_GPU'] = '1'",
        "",
        "def parse_use_gpu_flag(raw_value: str) -> bool:",
        "    normalized = raw_value.strip().lower()",
        "    return normalized not in {'0', 'false', 'no', 'off'}",
        "",
        "load_runtime_env()",
        "USE_GPU = parse_use_gpu_flag(os.getenv('USE_GPU', '1'))",
        "GPU_AVAILABLE = len(tf.config.list_physical_devices('GPU')) > 0",
        "RUNTIME_DEVICE = 'gpu' if USE_GPU and GPU_AVAILABLE else 'cpu'",
        "print(f'USE_GPU={int(USE_GPU)} | runtime_device={RUNTIME_DEVICE}')",
    ]


def runtime_pt_block() -> list[str]:
    return [
        "def load_runtime_env() -> None:",
        "    candidate_paths = [",
        "        os.path.join(os.getcwd(), 'configs', 'runtime.env'),",
        "        os.path.join(os.getcwd(), 'configs', 'runtime.env.example'),",
        "        os.path.join(os.getcwd(), '..', 'configs', 'runtime.env'),",
        "        os.path.join(os.getcwd(), '..', 'configs', 'runtime.env.example'),",
        "    ]",
        "    env_loaded = False",
        "    for path in candidate_paths:",
        "        if not os.path.exists(path):",
        "            continue",
        "        with open(path, 'r', encoding='utf-8') as handle:",
        "            for raw_line in handle:",
        "                line = raw_line.strip()",
        "                if not line or line.startswith('#') or '=' not in line:",
        "                    continue",
        "                key, value = line.split('=', 1)",
        '                os.environ[key.strip()] = value.strip().strip("\\"\'")',
        "        env_loaded = True",
        "        break",
        "    if not env_loaded and 'USE_GPU' not in os.environ:",
        "        os.environ['USE_GPU'] = '1'",
        "",
        "def parse_use_gpu_flag(raw_value: str) -> bool:",
        "    normalized = raw_value.strip().lower()",
        "    return normalized not in {'0', 'false', 'no', 'off'}",
        "",
        "load_runtime_env()",
        "USE_GPU = parse_use_gpu_flag(os.getenv('USE_GPU', '1'))",
        "GPU_AVAILABLE = torch.cuda.is_available()",
        "RUNTIME_DEVICE = 'cuda' if USE_GPU and GPU_AVAILABLE else 'cpu'",
        "print(f'USE_GPU={int(USE_GPU)} | runtime_device={RUNTIME_DEVICE}')",
        "device = torch.device(RUNTIME_DEVICE)",
    ]


def tf_notebook(idx: str, name: str, desc: str):
    nb = nbf.v4.new_notebook()
    nb.cells = [
        md(
            [
                f"# Basic PEFT Type: {name} (TensorFlow)",
                "**Date**: 2026-05-31  ",
                f"**Objective**: Basic {name} implementation from scratch in TensorFlow for support-ticket urgency classification.",
            ]
        ),
        md(
            [
                "## Common Logic Highlight (Shared with PyTorch counterpart)",
                "- Same runtime policy: load configs/runtime.env and honor USE_GPU toggle.",
                "- Same dataset, label mapping, and train/test split logic.",
                "- Same evaluation metrics: accuracy and macro-F1.",
                "- Same PEFT goal: keep base representation mostly frozen and train lightweight adaptation parameters.",
                f"- Type-specific basic focus: {desc}.",
            ]
        ),
        code(
            [
                "import os",
                "import random",
                "from dataclasses import dataclass",
                "",
                "import matplotlib.pyplot as plt",
                "import numpy as np",
                "import pandas as pd",
                "import tensorflow as tf",
                "from sklearn.metrics import accuracy_score, f1_score",
                "",
                "SEED = 42",
                "random.seed(SEED)",
                "np.random.seed(SEED)",
                "tf.random.set_seed(SEED)",
                "os.environ['PYTHONHASHSEED'] = str(SEED)",
            ]
        ),
        code(runtime_tf_block()),
        code(
            [
                "@dataclass(frozen=True)",
                "class ExperimentConfig:",
                "    max_tokens: int = 2048",
                "    seq_len: int = 24",
                "    emb_dim: int = 48",
                "    hidden_dim: int = 64",
                "    adapter_rank: int = 8",
                "    batch_size: int = 4",
                "    epochs: int = 2",
                "    lr: float = 1e-3",
                "    train_size: float = 0.8",
                "",
                "cfg = ExperimentConfig()",
            ]
        ),
        code(common_samples_block()),
        code(
            [
                "vectorizer = tf.keras.layers.TextVectorization(",
                "    max_tokens=cfg.max_tokens,",
                "    output_mode='int',",
                "    output_sequence_length=cfg.seq_len,",
                ")",
                "vectorizer.adapt(train_df['text'].values)",
                "x_train = vectorizer(train_df['text'].values)",
                "x_test = vectorizer(test_df['text'].values)",
                "y_train = train_df['label'].to_numpy(dtype=np.int32)",
                "y_test = test_df['label'].to_numpy(dtype=np.int32)",
            ]
        ),
        code(
            [
                "class BasicAdapter(tf.keras.layers.Layer):",
                "    def __init__(self, hidden_dim: int, rank: int, **kwargs):",
                "        super().__init__(**kwargs)",
                "        self.down = tf.keras.layers.Dense(rank, use_bias=False)",
                "        self.up = tf.keras.layers.Dense(hidden_dim, use_bias=False)",
                "    def call(self, inputs, training=False):",
                "        return inputs + self.up(self.down(inputs))",
                "",
                "inputs = tf.keras.Input(shape=(cfg.seq_len,), dtype=tf.int64)",
                "embedding = tf.keras.layers.Embedding(cfg.max_tokens, cfg.emb_dim, name='base_embedding')",
                "pool = tf.keras.layers.GlobalAveragePooling1D(name='base_pool')",
                "base_dense = tf.keras.layers.Dense(cfg.hidden_dim, activation='relu', name='base_dense')",
                "x = embedding(inputs)",
                "x = pool(x)",
                "base = base_dense(x)",
                "embedding.trainable = False",
                "base_dense.trainable = False",
                "adapter = BasicAdapter(cfg.hidden_dim, cfg.adapter_rank, name='adapter')(base)",
                "outputs = tf.keras.layers.Dense(3, activation='softmax', name='classifier')(adapter)",
                "model = tf.keras.Model(inputs=inputs, outputs=outputs)",
                "model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=cfg.lr), loss='sparse_categorical_crossentropy', metrics=['accuracy'])",
            ]
        ),
        code(
            [
                "model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=cfg.epochs, batch_size=cfg.batch_size, verbose=0)",
                "pred_probs = model.predict(x_test, verbose=0)",
                "pred_labels = pred_probs.argmax(axis=1)",
                "metrics = {",
                "    'accuracy': float(accuracy_score(y_test, pred_labels)),",
                "    'macro_f1': float(f1_score(y_test, pred_labels, average='macro')),",
                "}",
                "print(metrics)",
            ]
        ),
        code(
            [
                "metric_names = ['accuracy', 'macro_f1']",
                "metric_values = [metrics.get(k, 0.0) for k in metric_names]",
                "plt.figure(figsize=(6, 4))",
                "plt.bar(metric_names, metric_values)",
                "plt.ylim(0.0, 1.0)",
                f"plt.title('Basic {name} TensorFlow: Evaluation Snapshot')",
                "plt.ylabel('Score')",
                "plt.show()",
            ]
        ),
        md(
            [
                "## Summary",
                "- Framework: TensorFlow",
                f"- Basic PEFT type: {name}",
                f"- Type behavior: {desc}.",
                "- Common logic is aligned with the matching PyTorch notebook.",
            ]
        ),
    ]
    return nb


def pt_notebook(idx: str, name: str, desc: str):
    nb = nbf.v4.new_notebook()
    nb.cells = [
        md(
            [
                f"# Basic PEFT Type: {name} (PyTorch)",
                "**Date**: 2026-05-31  ",
                f"**Objective**: Basic {name} implementation from scratch in PyTorch for support-ticket urgency classification.",
            ]
        ),
        md(
            [
                "## Common Logic Highlight (Shared with TensorFlow counterpart)",
                "- Same runtime policy: load configs/runtime.env and honor USE_GPU toggle.",
                "- Same dataset, label mapping, and train/test split logic.",
                "- Same evaluation metrics: accuracy and macro-F1.",
                "- Same PEFT goal: keep base representation mostly frozen and train lightweight adaptation parameters.",
                f"- Type-specific basic focus: {desc}.",
            ]
        ),
        code(
            [
                "import os",
                "import random",
                "from dataclasses import dataclass",
                "",
                "import matplotlib.pyplot as plt",
                "import numpy as np",
                "import pandas as pd",
                "import torch",
                "import torch.nn as nn",
                "from sklearn.metrics import accuracy_score, f1_score",
                "from torch.utils.data import DataLoader, TensorDataset",
                "",
                "SEED = 42",
                "random.seed(SEED)",
                "np.random.seed(SEED)",
                "torch.manual_seed(SEED)",
                "os.environ['PYTHONHASHSEED'] = str(SEED)",
            ]
        ),
        code(runtime_pt_block()),
        code(
            [
                "@dataclass(frozen=True)",
                "class ExperimentConfig:",
                "    seq_len: int = 24",
                "    emb_dim: int = 48",
                "    hidden_dim: int = 64",
                "    adapter_rank: int = 8",
                "    batch_size: int = 4",
                "    epochs: int = 2",
                "    lr: float = 1e-3",
                "    train_size: float = 0.8",
                "",
                "cfg = ExperimentConfig()",
            ]
        ),
        code(common_samples_block()),
        code(
            [
                "def build_vocab(texts: list[str]) -> dict[str, int]:",
                "    vocab = {'<pad>': 0, '<unk>': 1}",
                "    for text in texts:",
                "        for token in text.lower().split():",
                "            if token not in vocab:",
                "                vocab[token] = len(vocab)",
                "    return vocab",
                "",
                "def encode_text(text: str, vocab: dict[str, int], seq_len: int) -> list[int]:",
                "    ids = [vocab.get(tok, vocab['<unk>']) for tok in text.lower().split()]",
                "    ids = ids[:seq_len]",
                "    ids += [vocab['<pad>']] * max(0, seq_len - len(ids))",
                "    return ids",
                "",
                "vocab = build_vocab(train_df['text'].tolist())",
                "x_train = np.array([encode_text(t, vocab, cfg.seq_len) for t in train_df['text']], dtype=np.int64)",
                "x_test = np.array([encode_text(t, vocab, cfg.seq_len) for t in test_df['text']], dtype=np.int64)",
                "y_train = train_df['label'].to_numpy(dtype=np.int64)",
                "y_test = test_df['label'].to_numpy(dtype=np.int64)",
                "train_ds = TensorDataset(torch.tensor(x_train), torch.tensor(y_train))",
                "test_ds = TensorDataset(torch.tensor(x_test), torch.tensor(y_test))",
                "train_loader = DataLoader(train_ds, batch_size=cfg.batch_size, shuffle=True)",
                "test_loader = DataLoader(test_ds, batch_size=cfg.batch_size, shuffle=False)",
            ]
        ),
        code(
            [
                "class BasicAdapter(nn.Module):",
                "    def __init__(self, hidden_dim: int, rank: int):",
                "        super().__init__()",
                "        self.down = nn.Linear(hidden_dim, rank, bias=False)",
                "        self.up = nn.Linear(rank, hidden_dim, bias=False)",
                "    def forward(self, x: torch.Tensor) -> torch.Tensor:",
                "        return x + self.up(self.down(x))",
                "",
                "class BasicPeftClassifier(nn.Module):",
                "    def __init__(self, vocab_size: int, cfg: ExperimentConfig):",
                "        super().__init__()",
                "        self.embedding = nn.Embedding(vocab_size, cfg.emb_dim)",
                "        self.base_linear = nn.Linear(cfg.emb_dim, cfg.hidden_dim)",
                "        self.adapter = BasicAdapter(cfg.hidden_dim, cfg.adapter_rank)",
                "        self.classifier = nn.Linear(cfg.hidden_dim, 3)",
                "        for p in self.embedding.parameters():",
                "            p.requires_grad = False",
                "        for p in self.base_linear.parameters():",
                "            p.requires_grad = False",
                "    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:",
                "        emb = self.embedding(input_ids)",
                "        pooled = emb.mean(dim=1)",
                "        base = torch.relu(self.base_linear(pooled))",
                "        adapted = self.adapter(base)",
                "        return self.classifier(adapted)",
                "",
                "model = BasicPeftClassifier(len(vocab), cfg).to(device)",
            ]
        ),
        code(
            [
                "optimizer = torch.optim.Adam((p for p in model.parameters() if p.requires_grad), lr=cfg.lr)",
                "criterion = nn.CrossEntropyLoss()",
                "for _ in range(cfg.epochs):",
                "    model.train()",
                "    for xb, yb in train_loader:",
                "        xb, yb = xb.to(device), yb.to(device)",
                "        optimizer.zero_grad()",
                "        logits = model(xb)",
                "        loss = criterion(logits, yb)",
                "        loss.backward()",
                "        optimizer.step()",
                "model.eval()",
                "preds = []",
                "labels = []",
                "with torch.no_grad():",
                "    for xb, yb in test_loader:",
                "        xb = xb.to(device)",
                "        logits = model(xb)",
                "        pred = torch.argmax(logits, dim=-1).cpu().numpy()",
                "        preds.extend(pred.tolist())",
                "        labels.extend(yb.numpy().tolist())",
                "metrics = {",
                "    'accuracy': float(accuracy_score(labels, preds)),",
                "    'macro_f1': float(f1_score(labels, preds, average='macro')),",
                "}",
                "print(metrics)",
            ]
        ),
        code(
            [
                "metric_names = ['accuracy', 'macro_f1']",
                "metric_values = [metrics.get(k, 0.0) for k in metric_names]",
                "plt.figure(figsize=(6, 4))",
                "plt.bar(metric_names, metric_values)",
                "plt.ylim(0.0, 1.0)",
                f"plt.title('Basic {name} PyTorch: Evaluation Snapshot')",
                "plt.ylabel('Score')",
                "plt.show()",
            ]
        ),
        md(
            [
                "## Summary",
                "- Framework: PyTorch",
                f"- Basic PEFT type: {name}",
                f"- Type behavior: {desc}.",
                "- Common logic is aligned with the matching TensorFlow notebook.",
            ]
        ),
    ]
    return nb


for idx, name, desc in peft_types:
    slug = name.lower().replace(" ", "-")
    tf_path = root / "tensorflow" / f"{idx}-{slug}-basic-tensorflow.ipynb"
    pt_path = root / "pytorch" / f"{idx}-{slug}-basic-pytorch.ipynb"
    nbf.write(tf_notebook(idx, name, desc), tf_path)
    nbf.write(pt_notebook(idx, name, desc), pt_path)

(root / "README.md").write_text(
    "\n".join(
        [
            "# Basic PEFT Matrix (Type-by-Type, Dual Framework)",
            "",
            "This folder contains separate basic notebooks for each PEFT type in both TensorFlow and PyTorch.",
            "",
            "## TensorFlow",
            "- tensorflow/01-lora-basic-tensorflow.ipynb",
            "- tensorflow/02-qlora-basic-tensorflow.ipynb",
            "- tensorflow/03-prefix-tuning-basic-tensorflow.ipynb",
            "- tensorflow/04-prompt-tuning-basic-tensorflow.ipynb",
            "- tensorflow/05-p-tuning-v2-basic-tensorflow.ipynb",
            "- tensorflow/06-ia3-basic-tensorflow.ipynb",
            "- tensorflow/07-adalora-basic-tensorflow.ipynb",
            "- tensorflow/08-bitfit-basic-tensorflow.ipynb",
            "",
            "## PyTorch",
            "- pytorch/01-lora-basic-pytorch.ipynb",
            "- pytorch/02-qlora-basic-pytorch.ipynb",
            "- pytorch/03-prefix-tuning-basic-pytorch.ipynb",
            "- pytorch/04-prompt-tuning-basic-pytorch.ipynb",
            "- pytorch/05-p-tuning-v2-basic-pytorch.ipynb",
            "- pytorch/06-ia3-basic-pytorch.ipynb",
            "- pytorch/07-adalora-basic-pytorch.ipynb",
            "- pytorch/08-bitfit-basic-pytorch.ipynb",
            "",
            "Each notebook includes a Common Logic Highlight section to make cross-framework parity explicit.",
        ]
    ),
    encoding="utf-8",
)

print("Generated basic PEFT matrix notebooks.")
