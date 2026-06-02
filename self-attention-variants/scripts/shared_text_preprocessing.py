from __future__ import annotations

from dataclasses import dataclass

import numpy as np

POSITIVE_TERMS = [
    "reliable",
    "scalable",
    "stable",
    "efficient",
    "robust",
    "accurate",
]

NEGATIVE_TERMS = [
    "noisy",
    "fragile",
    "unstable",
    "slow",
    "costly",
    "drifting",
]

TEMPLATES = [
    "{core} attention improves context handling for enterprise workloads",
    "team reports {core} inference behaviour in production traces",
    "analysis shows {core} routing across long document windows",
    "service indicates {core} retrieval quality for multilingual traffic",
]


@dataclass(frozen=True)
class PreprocessingConfig:
    num_samples: int = 256
    seq_len: int = 24
    max_vocab_size: int = 2048
    train_ratio: float = 0.8


@dataclass(frozen=True)
class PreprocessedTextData:
    train_token_ids: np.ndarray
    test_token_ids: np.ndarray
    y_train: np.ndarray
    y_test: np.ndarray
    vocab: dict[str, int]
    texts_train: list[str]
    texts_test: list[str]


def normalize_text(text: str) -> str:
    return " ".join(text.lower().strip().split())


def tokenize_text(text: str) -> list[str]:
    return normalize_text(text).split()


def build_text_dataset(
    cfg: PreprocessingConfig, rng: np.random.Generator
) -> tuple[list[str], np.ndarray]:
    texts: list[str] = []
    labels = np.zeros(cfg.num_samples, dtype=np.int64)
    for idx in range(cfg.num_samples):
        is_positive = idx % 2 == 0
        pool = POSITIVE_TERMS if is_positive else NEGATIVE_TERMS
        core = pool[int(rng.integers(0, len(pool)))]
        template = TEMPLATES[int(rng.integers(0, len(TEMPLATES)))]
        texts.append(template.format(core=core))
        labels[idx] = int(is_positive)
    return texts, labels


def build_vocabulary(train_texts: list[str], max_vocab_size: int) -> dict[str, int]:
    token_counts: dict[str, int] = {}
    for text in train_texts:
        for token in tokenize_text(text):
            token_counts[token] = token_counts.get(token, 0) + 1

    sorted_items = sorted(token_counts.items(), key=lambda item: (-item[1], item[0]))
    vocab: dict[str, int] = {"<PAD>": 0, "<UNK>": 1}
    for token, _ in sorted_items:
        if len(vocab) >= max_vocab_size:
            break
        vocab[token] = len(vocab)
    return vocab


def encode_and_pad(texts: list[str], vocab: dict[str, int], seq_len: int) -> np.ndarray:
    encoded = np.zeros((len(texts), seq_len), dtype=np.int64)
    unk_id = vocab["<UNK>"]
    for row_idx, text in enumerate(texts):
        token_ids = [vocab.get(token, unk_id) for token in tokenize_text(text)]
        trunc = token_ids[:seq_len]
        encoded[row_idx, : len(trunc)] = np.asarray(trunc, dtype=np.int64)
    return encoded


def prepare_text_data(cfg: PreprocessingConfig, seed: int = 42) -> PreprocessedTextData:
    rng = np.random.default_rng(seed)
    texts_all, y_all = build_text_dataset(cfg, rng)

    split = int(cfg.train_ratio * cfg.num_samples)
    texts_train = texts_all[:split]
    texts_test = texts_all[split:]
    y_train = y_all[:split]
    y_test = y_all[split:]

    vocab = build_vocabulary(texts_train, cfg.max_vocab_size)
    train_token_ids = encode_and_pad(texts_train, vocab, cfg.seq_len)
    test_token_ids = encode_and_pad(texts_test, vocab, cfg.seq_len)

    return PreprocessedTextData(
        train_token_ids=train_token_ids,
        test_token_ids=test_token_ids,
        y_train=y_train,
        y_test=y_test,
        vocab=vocab,
        texts_train=texts_train,
        texts_test=texts_test,
    )
