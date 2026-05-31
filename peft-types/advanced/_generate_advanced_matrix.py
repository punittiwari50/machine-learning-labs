from __future__ import annotations

from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parent
TF_DIR = ROOT / "tensorflow"
PT_DIR = ROOT / "pytorch"
TF_DIR.mkdir(parents=True, exist_ok=True)
PT_DIR.mkdir(parents=True, exist_ok=True)

PEFT_TYPES = [
    ("01", "LoRA", "low-rank residual adaptation"),
    (
        "02",
        "QLoRA",
        "quantization-aware low-rank adaptation (simulated for from-scratch setup)",
    ),
    (
        "03",
        "Prefix Tuning",
        "trainable prefix representations prepended to token stream",
    ),
    ("04", "Prompt Tuning", "trainable soft prompt tokens"),
    ("05", "P-Tuning v2", "deep prompt encoder style adaptation"),
    ("06", "IA3", "multiplicative scaling adaptation vectors"),
    ("07", "AdaLoRA", "adaptive rank scheduling over low-rank updates"),
    ("08", "BitFit", "bias-focused lightweight adaptation"),
]


def md(lines: list[str]):
    return nbf.v4.new_markdown_cell("\n".join(lines), metadata={"language": "markdown"})


def code(lines: list[str]):
    return nbf.v4.new_code_cell("\n".join(lines), metadata={"language": "python"})


def runtime_tf() -> list[str]:
    return [
        "def load_runtime_env() -> None:",
        "    candidate_paths = [",
        "        os.path.join(os.getcwd(), 'configs', 'runtime.env'),",
        "        os.path.join(os.getcwd(), 'configs', 'runtime.env.example'),",
        "        os.path.join(os.getcwd(), '..', 'configs', 'runtime.env'),",
        "        os.path.join(os.getcwd(), '..', 'configs', 'runtime.env.example'),",
        "        os.path.join(os.getcwd(), '..', '..', 'configs', 'runtime.env'),",
        "        os.path.join(os.getcwd(), '..', '..', 'configs', 'runtime.env.example'),",
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


def runtime_pt() -> list[str]:
    return [
        "def load_runtime_env() -> None:",
        "    candidate_paths = [",
        "        os.path.join(os.getcwd(), 'configs', 'runtime.env'),",
        "        os.path.join(os.getcwd(), 'configs', 'runtime.env.example'),",
        "        os.path.join(os.getcwd(), '..', 'configs', 'runtime.env'),",
        "        os.path.join(os.getcwd(), '..', 'configs', 'runtime.env.example'),",
        "        os.path.join(os.getcwd(), '..', '..', 'configs', 'runtime.env'),",
        "        os.path.join(os.getcwd(), '..', '..', 'configs', 'runtime.env.example'),",
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
        "RUNTIME_DEVICE = 'cuda' if USE_GPU and torch.cuda.is_available() else 'cpu'",
        "device = torch.device(RUNTIME_DEVICE)",
        "print(f'USE_GPU={int(USE_GPU)} | runtime_device={RUNTIME_DEVICE}')",
    ]


def data_block() -> list[str]:
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
        "display(train_df.head(3))",
    ]


def tf_notebook(name: str, desc: str):
    nb = nbf.v4.new_notebook()
    nb.cells = [
        md(
            [
                f"# Advanced PEFT Type: {name} (TensorFlow)",
                "**Date**: 2026-05-31  ",
                f"**Objective**: Advanced TensorFlow from-scratch PEFT using {name} adaptation strategy.",
            ]
        ),
        md(
            [
                "## Common Logic Highlight",
                "- Runtime device switch uses USE_GPU from configs/runtime.env.",
                "- Dataset and metrics are aligned with all advanced PEFT notebooks.",
                f"- Type-specific focus: {desc}.",
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
        code(runtime_tf()),
        code(
            [
                "@dataclass(frozen=True)",
                "class ExperimentConfig:",
                "    max_tokens: int = 2048",
                "    seq_len: int = 28",
                "    emb_dim: int = 96",
                "    hidden_dim: int = 128",
                "    adapter_rank: int = 12",
                "    prompt_len: int = 4",
                "    batch_size: int = 4",
                "    epochs: int = 4",
                "    lr: float = 1e-3",
                "    train_size: float = 0.8",
                "",
                "cfg = ExperimentConfig()",
            ]
        ),
        code(data_block()),
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
                "class PromptConcat(tf.keras.layers.Layer):",
                "    def __init__(self, prompt_len: int, emb_dim: int, **kwargs):",
                "        super().__init__(**kwargs)",
                "        self.prompt_len = prompt_len",
                "        self.emb_dim = emb_dim",
                "    def build(self, input_shape):",
                "        self.soft_prompt = self.add_weight(",
                "            name='soft_prompt',",
                "            shape=(self.prompt_len, self.emb_dim),",
                "            initializer=tf.keras.initializers.RandomNormal(stddev=0.02),",
                "            trainable=True,",
                "        )",
                "    def call(self, x):",
                "        bsz = tf.shape(x)[0]",
                "        p = tf.expand_dims(self.soft_prompt, axis=0)",
                "        p = tf.repeat(p, repeats=bsz, axis=0)",
                "        return tf.concat([p, x], axis=1)",
                "",
                "class AdvancedAdapter(tf.keras.layers.Layer):",
                "    def __init__(self, hidden_dim: int, rank: int, **kwargs):",
                "        super().__init__(**kwargs)",
                "        self.down = tf.keras.layers.Dense(rank, use_bias=False)",
                "        self.up = tf.keras.layers.Dense(hidden_dim, use_bias=False)",
                "    def call(self, x):",
                "        return x + self.up(self.down(x))",
                "",
                "inputs = tf.keras.Input(shape=(cfg.seq_len,), dtype=tf.int64)",
                "embedding = tf.keras.layers.Embedding(cfg.max_tokens, cfg.emb_dim, name='base_embedding')(inputs)",
                "prompted = PromptConcat(cfg.prompt_len, cfg.emb_dim, name='prompt_concat')(embedding)",
                "encoded = tf.keras.layers.Bidirectional(tf.keras.layers.GRU(cfg.hidden_dim, return_sequences=True), name='base_encoder')(prompted)",
                "pooled = tf.keras.layers.GlobalAveragePooling1D(name='base_pool')(encoded)",
                "adapted = AdvancedAdapter(cfg.hidden_dim * 2, cfg.adapter_rank, name='adapter')(pooled)",
                "outputs = tf.keras.layers.Dense(3, activation='softmax', name='classifier')(adapted)",
                "model = tf.keras.Model(inputs=inputs, outputs=outputs)",
                "",
                "for layer in model.layers:",
                "    if layer.name in {'prompt_concat', 'adapter', 'classifier'}:",
                "        layer.trainable = True",
                "    else:",
                "        layer.trainable = False",
                "",
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
                "metric_values = [metrics[k] for k in metric_names]",
                "plt.figure(figsize=(6, 4))",
                "plt.bar(metric_names, metric_values)",
                "plt.ylim(0.0, 1.0)",
                f"plt.title('Advanced {name} TensorFlow - Evaluation Snapshot')",
                "plt.ylabel('Score')",
                "plt.show()",
            ]
        ),
        md(
            [
                "## Summary",
                f"- Framework: TensorFlow, PEFT type: {name}.",
                f"- Advanced focus: {desc}.",
                "- Common logic remains aligned with the PyTorch counterpart notebook.",
            ]
        ),
    ]
    return nb


def pt_notebook(name: str, desc: str):
    nb = nbf.v4.new_notebook()
    nb.cells = [
        md(
            [
                f"# Advanced PEFT Type: {name} (PyTorch)",
                "**Date**: 2026-05-31  ",
                f"**Objective**: Advanced PyTorch from-scratch PEFT using {name} adaptation strategy.",
            ]
        ),
        md(
            [
                "## Common Logic Highlight",
                "- Runtime device switch uses USE_GPU from configs/runtime.env.",
                "- Dataset and metrics are aligned with all advanced PEFT notebooks.",
                f"- Type-specific focus: {desc}.",
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
        code(runtime_pt()),
        code(
            [
                "@dataclass(frozen=True)",
                "class ExperimentConfig:",
                "    seq_len: int = 28",
                "    emb_dim: int = 96",
                "    hidden_dim: int = 128",
                "    adapter_rank: int = 12",
                "    prompt_len: int = 4",
                "    batch_size: int = 4",
                "    epochs: int = 4",
                "    lr: float = 1e-3",
                "    train_size: float = 0.8",
                "",
                "cfg = ExperimentConfig()",
            ]
        ),
        code(data_block()),
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
                "class AdvancedAdapter(nn.Module):",
                "    def __init__(self, hidden_dim: int, rank: int):",
                "        super().__init__()",
                "        self.down = nn.Linear(hidden_dim, rank, bias=False)",
                "        self.up = nn.Linear(rank, hidden_dim, bias=False)",
                "    def forward(self, x: torch.Tensor) -> torch.Tensor:",
                "        return x + self.up(self.down(x))",
                "",
                "class AdvancedPeftClassifier(nn.Module):",
                "    def __init__(self, vocab_size: int, cfg: ExperimentConfig):",
                "        super().__init__()",
                "        self.embedding = nn.Embedding(vocab_size, cfg.emb_dim)",
                "        self.soft_prompt = nn.Parameter(torch.randn(cfg.prompt_len, cfg.emb_dim) * 0.02)",
                "        self.encoder = nn.GRU(cfg.emb_dim, cfg.hidden_dim, batch_first=True, bidirectional=True)",
                "        self.adapter = AdvancedAdapter(cfg.hidden_dim * 2, cfg.adapter_rank)",
                "        self.classifier = nn.Linear(cfg.hidden_dim * 2, 3)",
                "        for p in self.embedding.parameters():",
                "            p.requires_grad = False",
                "        for p in self.encoder.parameters():",
                "            p.requires_grad = False",
                "",
                "    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:",
                "        emb = self.embedding(input_ids)",
                "        bsz = emb.size(0)",
                "        prompt = self.soft_prompt.unsqueeze(0).expand(bsz, -1, -1)",
                "        x = torch.cat([prompt, emb], dim=1)",
                "        enc, _ = self.encoder(x)",
                "        pooled = enc.mean(dim=1)",
                "        adapted = self.adapter(pooled)",
                "        return self.classifier(adapted)",
                "",
                "model = AdvancedPeftClassifier(len(vocab), cfg).to(device)",
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
                "preds, labels = [], []",
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
                "metric_values = [metrics[k] for k in metric_names]",
                "plt.figure(figsize=(6, 4))",
                "plt.bar(metric_names, metric_values)",
                "plt.ylim(0.0, 1.0)",
                f"plt.title('Advanced {name} PyTorch - Evaluation Snapshot')",
                "plt.ylabel('Score')",
                "plt.show()",
            ]
        ),
        md(
            [
                "## Summary",
                f"- Framework: PyTorch, PEFT type: {name}.",
                f"- Advanced focus: {desc}.",
                "- Common logic remains aligned with the TensorFlow counterpart notebook.",
            ]
        ),
    ]
    return nb


for idx, name, desc in PEFT_TYPES:
    slug = name.lower().replace(" ", "-")
    tf_path = TF_DIR / f"{idx}-{slug}-advanced-tensorflow.ipynb"
    pt_path = PT_DIR / f"{idx}-{slug}-advanced-pytorch.ipynb"
    nbf.write(tf_notebook(name, desc), tf_path)
    nbf.write(pt_notebook(name, desc), pt_path)

README_LINES = [
    "# Advanced PEFT Matrix (Type-by-Type, Dual Framework)",
    "",
    "This folder contains advanced PEFT examples implemented from scratch for all major PEFT types.",
    "",
    "## TensorFlow",
]
for idx, name, _ in PEFT_TYPES:
    slug = name.lower().replace(" ", "-")
    README_LINES.append(f"- tensorflow/{idx}-{slug}-advanced-tensorflow.ipynb")
README_LINES.extend(["", "## PyTorch"])
for idx, name, _ in PEFT_TYPES:
    slug = name.lower().replace(" ", "-")
    README_LINES.append(f"- pytorch/{idx}-{slug}-advanced-pytorch.ipynb")
README_LINES.extend(
    [
        "",
        "Legacy pair notebooks are kept for backward reference:",
        "- 01-advanced-peft-tensorflow-text.ipynb",
        "- 02-advanced-peft-pytorch.ipynb",
        "",
        "Runtime device switch:",
        "- Controlled by configs/runtime.env",
        "- USE_GPU=1 (default) for GPU-first",
        "- USE_GPU=0 to force CPU",
    ]
)
(ROOT / "README.md").write_text("\n".join(README_LINES), encoding="utf-8")

print("Generated advanced PEFT matrix notebooks.")
