from __future__ import annotations

import math
import os
from dataclasses import dataclass

import numpy as np
import torch
import torch.nn.functional as F

from shared_text_preprocessing import PreprocessingConfig, prepare_text_data


@dataclass(frozen=True)
class ExperimentConfig:
    d_model: int = 32
    num_heads: int = 4
    learning_rate: float = 0.05
    epochs: int = 120
    seed: int = 42


def parse_use_gpu_flag(raw_value: str) -> bool:
    normalized = raw_value.strip().lower()
    return normalized not in {"0", "false", "no", "off"}


def resolve_device() -> torch.device:
    use_gpu = parse_use_gpu_flag(os.getenv("USE_GPU", "1"))
    if use_gpu and torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def build_embeddings(
    token_ids: np.ndarray,
    vocab_size: int,
    d_model: int,
    device: torch.device,
    seed: int,
) -> torch.Tensor:
    generator = torch.Generator(device=device)
    generator.manual_seed(seed)

    emb = torch.nn.Embedding(vocab_size, d_model, device=device)
    with torch.no_grad():
        emb.weight.copy_(
            torch.randn(vocab_size, d_model, generator=generator, device=device) * 0.2
        )

    token_tensor = torch.tensor(token_ids, dtype=torch.long, device=device)
    return emb(token_tensor)


def project_qkv(
    x: torch.Tensor, d_model: int, seed: int
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    generator = torch.Generator(device=x.device)
    generator.manual_seed(seed + 7)

    w_q = torch.randn(d_model, d_model, generator=generator, device=x.device) * 0.2
    w_k = torch.randn(d_model, d_model, generator=generator, device=x.device) * 0.2
    w_v = torch.randn(d_model, d_model, generator=generator, device=x.device) * 0.2
    return x @ w_q, x @ w_k, x @ w_v


def scaled_dot_product_attention(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor]:
    scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(q.size(-1))
    weights = torch.softmax(scores, dim=-1)
    return torch.matmul(weights, v), weights


def multi_head_attention(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    num_heads: int,
) -> tuple[torch.Tensor, torch.Tensor]:
    batch, seq_len, d_model = q.shape
    if d_model % num_heads != 0:
        raise ValueError(
            f"d_model ({d_model}) must be divisible by num_heads ({num_heads})."
        )

    head_dim = d_model // num_heads
    qh = q.view(batch, seq_len, num_heads, head_dim).permute(0, 2, 1, 3)
    kh = k.view(batch, seq_len, num_heads, head_dim).permute(0, 2, 1, 3)
    vh = v.view(batch, seq_len, num_heads, head_dim).permute(0, 2, 1, 3)

    scores = torch.matmul(qh, kh.transpose(-2, -1)) / math.sqrt(head_dim)
    weights = torch.softmax(scores, dim=-1)
    out = torch.matmul(weights, vh)
    out = out.permute(0, 2, 1, 3).reshape(batch, seq_len, d_model)
    return out, weights


def pooled_features(attn_out: torch.Tensor) -> torch.Tensor:
    return attn_out.mean(dim=1)


def train_binary_head(
    x_feat_train: torch.Tensor,
    y_train: np.ndarray,
    learning_rate: float,
    epochs: int,
) -> torch.nn.Linear:
    model = torch.nn.Linear(x_feat_train.size(1), 1, device=x_feat_train.device)
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
    y_train_t = torch.tensor(
        y_train, dtype=torch.float32, device=x_feat_train.device
    ).view(-1, 1)

    for _ in range(epochs):
        logits = model(x_feat_train)
        loss = F.binary_cross_entropy_with_logits(logits, y_train_t)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    return model


def evaluate_binary_classifier(
    x_feat: torch.Tensor,
    y_true: np.ndarray,
    model: torch.nn.Linear,
) -> dict[str, float]:
    with torch.no_grad():
        logits = model(x_feat)
        probs = torch.sigmoid(logits)
        preds = (probs >= 0.5).to(torch.int64).view(-1).cpu().numpy()
    accuracy = float((preds == y_true).mean())
    return {"accuracy": accuracy}


def run_pipeline() -> dict[str, object]:
    exp_cfg = ExperimentConfig()
    prep_cfg = PreprocessingConfig(num_samples=256, seq_len=24)
    torch.manual_seed(exp_cfg.seed)
    np.random.seed(exp_cfg.seed)

    data = prepare_text_data(prep_cfg, seed=exp_cfg.seed)
    device = resolve_device()

    x_train = build_embeddings(
        data.train_token_ids,
        len(data.vocab),
        exp_cfg.d_model,
        device,
        seed=exp_cfg.seed,
    )
    x_test = build_embeddings(
        data.test_token_ids,
        len(data.vocab),
        exp_cfg.d_model,
        device,
        seed=exp_cfg.seed + 1,
    )

    q_train, k_train, v_train = project_qkv(x_train, exp_cfg.d_model, seed=exp_cfg.seed)
    q_test, k_test, v_test = project_qkv(x_test, exp_cfg.d_model, seed=exp_cfg.seed)

    attn_train, _ = multi_head_attention(q_train, k_train, v_train, exp_cfg.num_heads)
    attn_test, _ = multi_head_attention(q_test, k_test, v_test, exp_cfg.num_heads)

    x_feat_train = pooled_features(attn_train).detach()
    x_feat_test = pooled_features(attn_test).detach()

    model = train_binary_head(
        x_feat_train,
        data.y_train,
        exp_cfg.learning_rate,
        exp_cfg.epochs,
    )
    metrics = evaluate_binary_classifier(x_feat_test, data.y_test, model)
    return {"device": str(device), **metrics}


def main() -> None:
    metrics = run_pipeline()
    print({"library": "pytorch", **metrics})


if __name__ == "__main__":
    main()
