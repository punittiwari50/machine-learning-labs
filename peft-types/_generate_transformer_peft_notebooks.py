from __future__ import annotations

from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parent
BASIC_DIR = ROOT / "transformer-basic"
ADV_DIR = ROOT / "transformer-advance"

PEFT_TYPES = [
    ("01", "LoRA", "low-rank adaptation"),
    ("02", "QLoRA", "quantized low-rank adaptation (TF: simulated)"),
    ("03", "Prefix Tuning", "trainable prefix vectors prepended to sequence"),
    ("04", "Prompt Tuning", "trainable soft prompt tokens"),
    ("05", "P-Tuning v2", "prompt encoder style adaptation"),
    ("06", "IA3", "multiplicative vector scaling"),
    ("07", "AdaLoRA", "rank-adaptive low-rank adaptation"),
    ("08", "BitFit", "bias-focused adaptation"),
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


def tf_before_after_cells() -> list:
    return [
        md(
            [
                "## Before vs After PEFT (Code Example)",
                "- Before PEFT: full fine-tuning (all backbone parameters trainable).",
                "- After PEFT: freeze backbone and train only prompt/adapter/head.",
            ]
        ),
        code(
            [
                "class DemoFullFineTune(tf.keras.Model):",
                "    def __init__(self):",
                "        super().__init__()",
                "        self.emb = tf.keras.layers.Embedding(1024, 64)",
                "        self.ff = tf.keras.layers.Dense(64, activation='relu')",
                "        self.cls = tf.keras.layers.Dense(3)",
                "    def call(self, x):",
                "        h = self.emb(x)",
                "        h = tf.reduce_mean(h, axis=1)",
                "        return self.cls(self.ff(h))",
                "",
                "class DemoPeft(tf.keras.Model):",
                "    def __init__(self):",
                "        super().__init__()",
                "        self.emb = tf.keras.layers.Embedding(1024, 64)",
                "        self.ff = tf.keras.layers.Dense(64, activation='relu')",
                "        self.adapter_down = tf.keras.layers.Dense(8, use_bias=False)",
                "        self.adapter_up = tf.keras.layers.Dense(64, use_bias=False)",
                "        self.cls = tf.keras.layers.Dense(3)",
                "    def call(self, x):",
                "        h = self.emb(x)",
                "        h = tf.reduce_mean(h, axis=1)",
                "        base = self.ff(h)",
                "        adapted = base + self.adapter_up(self.adapter_down(base))",
                "        return self.cls(adapted)",
                "",
                "def count_trainable_tf(model: tf.keras.Model) -> int:",
                "    return int(np.sum([np.prod(v.shape) for v in model.trainable_weights]))",
                "",
                "sample_ids = tf.ones((2, 12), dtype=tf.int32)",
                "before_impl = DemoFullFineTune(); _ = before_impl(sample_ids)",
                "after_impl = DemoPeft(); _ = after_impl(sample_ids)",
                "after_impl.emb.trainable = False; after_impl.ff.trainable = False",
                "before_params = count_trainable_tf(before_impl)",
                "after_params = count_trainable_tf(after_impl)",
                "reduction = 1 - (after_params / before_params)",
                "print({'before_trainable': before_params, 'after_trainable': after_params, 'reduction_ratio': round(float(reduction), 4)})",
            ]
        ),
    ]


def pt_before_after_cells() -> list:
    return [
        md(
            [
                "## Before vs After PEFT (Code Example)",
                "- Before PEFT: full fine-tuning (all backbone parameters trainable).",
                "- After PEFT: freeze backbone and train only prompt/adapter/head.",
            ]
        ),
        code(
            [
                "class DemoFullFineTune(nn.Module):",
                "    def __init__(self):",
                "        super().__init__()",
                "        self.emb = nn.Embedding(1024, 64)",
                "        self.ff = nn.Linear(64, 64)",
                "        self.cls = nn.Linear(64, 3)",
                "    def forward(self, x: torch.Tensor) -> torch.Tensor:",
                "        h = self.emb(x).mean(dim=1)",
                "        return self.cls(torch.relu(self.ff(h)))",
                "",
                "class DemoPeft(nn.Module):",
                "    def __init__(self):",
                "        super().__init__()",
                "        self.emb = nn.Embedding(1024, 64)",
                "        self.ff = nn.Linear(64, 64)",
                "        self.adapter_down = nn.Linear(64, 8, bias=False)",
                "        self.adapter_up = nn.Linear(8, 64, bias=False)",
                "        self.cls = nn.Linear(64, 3)",
                "    def forward(self, x: torch.Tensor) -> torch.Tensor:",
                "        h = self.emb(x).mean(dim=1)",
                "        base = torch.relu(self.ff(h))",
                "        adapted = base + self.adapter_up(self.adapter_down(base))",
                "        return self.cls(adapted)",
                "",
                "def count_trainable_pt(model: nn.Module) -> int:",
                "    return sum(p.numel() for p in model.parameters() if p.requires_grad)",
                "",
                "sample_ids = torch.ones((2, 12), dtype=torch.long)",
                "before_impl = DemoFullFineTune(); _ = before_impl(sample_ids)",
                "after_impl = DemoPeft(); _ = after_impl(sample_ids)",
                "for p in after_impl.emb.parameters(): p.requires_grad = False",
                "for p in after_impl.ff.parameters(): p.requires_grad = False",
                "before_params = count_trainable_pt(before_impl)",
                "after_params = count_trainable_pt(after_impl)",
                "reduction = 1 - (after_params / before_params)",
                "print({'before_trainable': before_params, 'after_trainable': after_params, 'reduction_ratio': round(float(reduction), 4)})",
            ]
        ),
    ]


def tf_notebook(peft_name: str, peft_desc: str, tier: str):
    advanced = tier == "advance"
    emb = 96 if advanced else 64
    ff_dim = 192 if advanced else 128
    rank = 12 if advanced else 8
    prompt_len = 4 if advanced else 2
    epochs = 4 if advanced else 3

    nb = nbf.v4.new_notebook()
    nb.cells = [
        md(
            [
                f"# Transformer {tier.capitalize()} PEFT: {peft_name} (TensorFlow)",
                "**Date**: 2026-05-31  ",
                f"**Objective**: {tier.capitalize()} transformer-based PEFT using {peft_name} pattern in TensorFlow.",
            ]
        ),
        md(
            [
                "## Common Logic Highlight",
                "- Same runtime switch policy using USE_GPU from configs/runtime.env.",
                "- Same project dataset and metrics for cross-framework comparison.",
                f"- Type focus: {peft_desc}.",
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
                "    vocab_size: int = 1024",
                "    seq_len: int = 24",
                f"    emb_dim: int = {emb}",
                "    heads: int = 4",
                f"    ff_dim: int = {ff_dim}",
                f"    adapter_rank: int = {rank}",
                f"    prompt_len: int = {prompt_len}",
                "    num_labels: int = 3",
                "    batch_size: int = 4",
                f"    epochs: int = {epochs}",
                "    lr: float = 1e-3",
                "    train_size: float = 0.8",
                "",
                "cfg = ExperimentConfig()",
            ]
        ),
        *tf_before_after_cells(),
        code(data_block()),
        code(
            [
                "def build_vocab(texts: list[str], vocab_size: int) -> dict[str, int]:",
                "    vocab = {'<pad>': 0, '<unk>': 1}",
                "    for text in texts:",
                "        for token in text.lower().split():",
                "            if token not in vocab and len(vocab) < vocab_size:",
                "                vocab[token] = len(vocab)",
                "    return vocab",
                "",
                "def encode_text(text: str, vocab: dict[str, int], seq_len: int) -> list[int]:",
                "    ids = [vocab.get(t, vocab['<unk>']) for t in text.lower().split()]",
                "    ids = ids[:seq_len]",
                "    ids += [vocab['<pad>']] * max(0, seq_len - len(ids))",
                "    return ids",
                "",
                "vocab = build_vocab(train_df['text'].tolist(), cfg.vocab_size)",
                "x_train = np.array([encode_text(t, vocab, cfg.seq_len) for t in train_df['text']], dtype=np.int32)",
                "x_test = np.array([encode_text(t, vocab, cfg.seq_len) for t in test_df['text']], dtype=np.int32)",
                "y_train = train_df['label'].to_numpy(dtype=np.int32)",
                "y_test = test_df['label'].to_numpy(dtype=np.int32)",
            ]
        ),
        code(
            [
                "class TransformerBlock(tf.keras.layers.Layer):",
                "    def __init__(self, emb_dim: int, heads: int, ff_dim: int, **kwargs):",
                "        super().__init__(**kwargs)",
                "        self.attn = tf.keras.layers.MultiHeadAttention(num_heads=heads, key_dim=emb_dim // heads)",
                "        self.ffn = tf.keras.Sequential([",
                "            tf.keras.layers.Dense(ff_dim, activation='relu'),",
                "            tf.keras.layers.Dense(emb_dim),",
                "        ])",
                "        self.norm1 = tf.keras.layers.LayerNormalization(epsilon=1e-6)",
                "        self.norm2 = tf.keras.layers.LayerNormalization(epsilon=1e-6)",
                "    def call(self, x, training=False):",
                "        h = self.attn(x, x, training=training)",
                "        x = self.norm1(x + h)",
                "        h2 = self.ffn(x, training=training)",
                "        return self.norm2(x + h2)",
                "",
                "class SoftPromptConcat(tf.keras.layers.Layer):",
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
                "    def call(self, token_embeddings):",
                "        batch_size = tf.shape(token_embeddings)[0]",
                "        prompt = tf.expand_dims(self.soft_prompt, axis=0)",
                "        prompt = tf.repeat(prompt, repeats=batch_size, axis=0)",
                "        return tf.concat([prompt, token_embeddings], axis=1)",
                "",
                "class AdapterLayer(tf.keras.layers.Layer):",
                "    def __init__(self, hidden_dim: int, rank: int, **kwargs):",
                "        super().__init__(**kwargs)",
                "        self.down = tf.keras.layers.Dense(rank, use_bias=False)",
                "        self.up = tf.keras.layers.Dense(hidden_dim, use_bias=False)",
                "    def call(self, x):",
                "        return x + self.up(self.down(x))",
                "",
                "inp = tf.keras.Input(shape=(cfg.seq_len,), dtype=tf.int32)",
                "tok = tf.keras.layers.Embedding(cfg.vocab_size, cfg.emb_dim, name='tok_emb')(inp)",
                "x = SoftPromptConcat(cfg.prompt_len, cfg.emb_dim, name='soft_prompt_concat')(tok)",
                "x = TransformerBlock(cfg.emb_dim, cfg.heads, cfg.ff_dim, name='encoder')(x)",
                "pooled = tf.keras.layers.GlobalAveragePooling1D(name='pool')(x)",
                "adapted = AdapterLayer(cfg.emb_dim, cfg.adapter_rank, name='adapter')(pooled)",
                "out = tf.keras.layers.Dense(cfg.num_labels, activation='softmax', name='classifier')(adapted)",
                "model = tf.keras.Model(inp, out)",
                "for layer in model.layers:",
                "    if layer.name in {'soft_prompt_concat', 'adapter', 'classifier'}:",
                "        layer.trainable = True",
                "    else:",
                "        layer.trainable = False",
                "model.compile(optimizer=tf.keras.optimizers.Adam(cfg.lr), loss='sparse_categorical_crossentropy', metrics=['accuracy'])",
            ]
        ),
        code(
            [
                "model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=cfg.epochs, batch_size=cfg.batch_size, verbose=0)",
                "pred = model.predict(x_test, verbose=0).argmax(axis=1)",
                "metrics = {",
                "    'accuracy': float(accuracy_score(y_test, pred)),",
                "    'macro_f1': float(f1_score(y_test, pred, average='macro')),",
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
                f"plt.title('Transformer {tier.capitalize()} {peft_name} TensorFlow - Metrics')",
                "plt.ylabel('Score')",
                "plt.show()",
            ]
        ),
        md(
            [
                "## Summary",
                f"- {peft_name} perspective: {peft_desc}.",
                "- Transformer backbone remains mostly frozen for PEFT behavior.",
                "- Shared dataset and metrics keep comparison aligned across frameworks.",
            ]
        ),
    ]
    return nb


def pt_notebook(peft_name: str, peft_desc: str, tier: str):
    advanced = tier == "advance"
    emb = 96 if advanced else 64
    ff_dim = 192 if advanced else 128
    rank = 12 if advanced else 8
    prompt_len = 4 if advanced else 2
    epochs = 4 if advanced else 3

    nb = nbf.v4.new_notebook()
    nb.cells = [
        md(
            [
                f"# Transformer {tier.capitalize()} PEFT: {peft_name} (PyTorch)",
                "**Date**: 2026-05-31  ",
                f"**Objective**: {tier.capitalize()} transformer-based PEFT using {peft_name} pattern in PyTorch.",
            ]
        ),
        md(
            [
                "## Common Logic Highlight",
                "- Same runtime switch policy using USE_GPU from configs/runtime.env.",
                "- Same project dataset and metrics for cross-framework comparison.",
                f"- Type focus: {peft_desc}.",
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
                "    vocab_size: int = 1024",
                "    seq_len: int = 24",
                f"    emb_dim: int = {emb}",
                "    heads: int = 4",
                f"    ff_dim: int = {ff_dim}",
                "    num_layers: int = 2",
                f"    adapter_rank: int = {rank}",
                f"    prompt_len: int = {prompt_len}",
                "    num_labels: int = 3",
                "    batch_size: int = 4",
                f"    epochs: int = {epochs}",
                "    lr: float = 1e-3",
                "    train_size: float = 0.8",
                "",
                "cfg = ExperimentConfig()",
            ]
        ),
        *pt_before_after_cells(),
        code(data_block()),
        code(
            [
                "def build_vocab(texts: list[str], vocab_size: int) -> dict[str, int]:",
                "    vocab = {'<pad>': 0, '<unk>': 1}",
                "    for text in texts:",
                "        for token in text.lower().split():",
                "            if token not in vocab and len(vocab) < vocab_size:",
                "                vocab[token] = len(vocab)",
                "    return vocab",
                "",
                "def encode_text(text: str, vocab: dict[str, int], seq_len: int) -> list[int]:",
                "    ids = [vocab.get(t, vocab['<unk>']) for t in text.lower().split()]",
                "    ids = ids[:seq_len]",
                "    ids += [vocab['<pad>']] * max(0, seq_len - len(ids))",
                "    return ids",
                "",
                "vocab = build_vocab(train_df['text'].tolist(), cfg.vocab_size)",
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
                "class Adapter(nn.Module):",
                "    def __init__(self, hidden_dim: int, rank: int):",
                "        super().__init__()",
                "        self.down = nn.Linear(hidden_dim, rank, bias=False)",
                "        self.up = nn.Linear(rank, hidden_dim, bias=False)",
                "    def forward(self, x: torch.Tensor) -> torch.Tensor:",
                "        return x + self.up(self.down(x))",
                "",
                "class TransformerPeft(nn.Module):",
                "    def __init__(self, cfg: ExperimentConfig):",
                "        super().__init__()",
                "        self.cfg = cfg",
                "        self.tok_emb = nn.Embedding(cfg.vocab_size, cfg.emb_dim)",
                "        self.pos_emb = nn.Embedding(cfg.seq_len + cfg.prompt_len, cfg.emb_dim)",
                "        self.soft_prompt = nn.Parameter(torch.randn(cfg.prompt_len, cfg.emb_dim) * 0.02)",
                "        enc_layer = nn.TransformerEncoderLayer(",
                "            d_model=cfg.emb_dim,",
                "            nhead=cfg.heads,",
                "            dim_feedforward=cfg.ff_dim,",
                "            dropout=0.1,",
                "            batch_first=True,",
                "        )",
                "        self.encoder = nn.TransformerEncoder(enc_layer, num_layers=cfg.num_layers)",
                "        self.adapter = Adapter(cfg.emb_dim, cfg.adapter_rank)",
                "        self.classifier = nn.Linear(cfg.emb_dim, cfg.num_labels)",
                "        for p in self.tok_emb.parameters():",
                "            p.requires_grad = False",
                "        for p in self.pos_emb.parameters():",
                "            p.requires_grad = False",
                "        for p in self.encoder.parameters():",
                "            p.requires_grad = False",
                "",
                "    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:",
                "        bsz, seqlen = input_ids.shape",
                "        tok = self.tok_emb(input_ids)",
                "        prompt = self.soft_prompt.unsqueeze(0).expand(bsz, -1, -1)",
                "        x = torch.cat([prompt, tok], dim=1)",
                "        pos = torch.arange(x.size(1), device=input_ids.device).unsqueeze(0).expand(bsz, -1)",
                "        x = x + self.pos_emb(pos)",
                "        x = self.encoder(x)",
                "        pooled = x.mean(dim=1)",
                "        adapted = self.adapter(pooled)",
                "        return self.classifier(adapted)",
                "",
                "model = TransformerPeft(cfg).to(device)",
            ]
        ),
        code(
            [
                "optim = torch.optim.Adam((p for p in model.parameters() if p.requires_grad), lr=cfg.lr)",
                "loss_fn = nn.CrossEntropyLoss()",
                "for _ in range(cfg.epochs):",
                "    model.train()",
                "    for xb, yb in train_loader:",
                "        xb, yb = xb.to(device), yb.to(device)",
                "        optim.zero_grad()",
                "        logits = model(xb)",
                "        loss = loss_fn(logits, yb)",
                "        loss.backward()",
                "        optim.step()",
                "model.eval()",
                "preds, labels = [], []",
                "with torch.no_grad():",
                "    for xb, yb in test_loader:",
                "        xb = xb.to(device)",
                "        pred = torch.argmax(model(xb), dim=-1).cpu().numpy()",
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
                f"plt.title('Transformer {tier.capitalize()} {peft_name} PyTorch - Metrics')",
                "plt.ylabel('Score')",
                "plt.show()",
            ]
        ),
        md(
            [
                "## Summary",
                f"- {peft_name} perspective: {peft_desc}.",
                "- Transformer backbone remains mostly frozen for PEFT behavior.",
                "- Shared dataset and metrics keep comparison aligned across frameworks.",
            ]
        ),
    ]
    return nb


def ensure_subdirs(base_dir: Path) -> tuple[Path, Path]:
    tf_dir = base_dir / "tensorflow"
    pt_dir = base_dir / "pytorch"
    tf_dir.mkdir(parents=True, exist_ok=True)
    pt_dir.mkdir(parents=True, exist_ok=True)
    return tf_dir, pt_dir


def write_tier(base_dir: Path, tier: str) -> None:
    tf_dir, pt_dir = ensure_subdirs(base_dir)
    for idx, name, desc in PEFT_TYPES:
        slug = name.lower().replace(" ", "-")
        tf_path = tf_dir / f"{idx}-{slug}-transformer-{tier}-tensorflow.ipynb"
        pt_path = pt_dir / f"{idx}-{slug}-transformer-{tier}-pytorch.ipynb"
        nbf.write(tf_notebook(name, desc, tier), tf_path)
        nbf.write(pt_notebook(name, desc, tier), pt_path)


def write_readme(base_dir: Path, tier: str) -> None:
    title = f"Transformer {tier.capitalize()} Matrix (Type-by-Type, Dual Framework)"
    lines = [
        f"# {title}",
        "",
        f"This folder contains transformer-based {tier} PEFT notebooks for all major PEFT types in TensorFlow and PyTorch.",
        "",
        "## TensorFlow",
    ]
    for idx, name, _ in PEFT_TYPES:
        slug = name.lower().replace(" ", "-")
        lines.append(f"- tensorflow/{idx}-{slug}-transformer-{tier}-tensorflow.ipynb")
    lines.extend(["", "## PyTorch"])
    for idx, name, _ in PEFT_TYPES:
        slug = name.lower().replace(" ", "-")
        lines.append(f"- pytorch/{idx}-{slug}-transformer-{tier}-pytorch.ipynb")
    lines.extend(
        [
            "",
            "All notebooks use the same task, runtime policy, and evaluation structure for easy comparison.",
        ]
    )
    (base_dir / "README.md").write_text("\n".join(lines), encoding="utf-8")


write_tier(BASIC_DIR, "basic")
write_tier(ADV_DIR, "advance")
write_readme(BASIC_DIR, "basic")
write_readme(ADV_DIR, "advance")

print("Generated transformer basic and advance type-wise matrices.")
