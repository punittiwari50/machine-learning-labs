from __future__ import annotations

import math
import os
import time
from dataclasses import dataclass

import numpy as np
import torch

from shared_text_preprocessing import PreprocessingConfig, prepare_text_data


@dataclass(frozen=True)
class ExperimentConfig:
    num_samples: int = 64
    seq_len: int = 128
    d_model: int = 48
    local_window: int = 8
    temperature_grid_size: int = 31
    seed: int = 42


def parse_use_gpu_flag(raw_value: str) -> bool:
    normalized = raw_value.strip().lower()
    return normalized not in {"0", "false", "no", "off"}


def resolve_device() -> torch.device:
    use_gpu = parse_use_gpu_flag(os.getenv("USE_GPU", "1"))
    if use_gpu and torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def init_projection_weights(
    d_model: int,
    device: torch.device,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    w_q = torch.randn(d_model, d_model, device=device) * 0.2
    w_k = torch.randn(d_model, d_model, device=device) * 0.2
    w_v = torch.randn(d_model, d_model, device=device) * 0.2
    return w_q, w_k, w_v


def apply_qkv_projection(
    x: torch.Tensor,
    w_q: torch.Tensor,
    w_k: torch.Tensor,
    w_v: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    return x @ w_q, x @ w_k, x @ w_v


def dense_attention(q: torch.Tensor, k: torch.Tensor, v: torch.Tensor) -> torch.Tensor:
    scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(q.size(-1))
    weights = torch.softmax(scores, dim=-1)
    return torch.matmul(weights, v)


def sparse_with_temperature(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    window: int,
    temperature: float,
) -> torch.Tensor:
    batch, seq_len, _ = q.shape
    scores = torch.full((batch, seq_len, seq_len), -1e9, device=q.device)
    raw = torch.matmul(q, k.transpose(-2, -1)) / (math.sqrt(q.size(-1)) * temperature)
    for i in range(seq_len):
        lo = max(0, i - window)
        hi = min(seq_len, i + window + 1)
        scores[:, i, lo:hi] = raw[:, i, lo:hi]
    weights = torch.softmax(scores, dim=-1)
    return torch.matmul(weights, v)


def linear_attention(q: torch.Tensor, k: torch.Tensor, v: torch.Tensor) -> torch.Tensor:
    q_phi = torch.relu(q) + 1e-3
    k_phi = torch.relu(k) + 1e-3
    kv = torch.einsum("bnd,bne->bde", k_phi, v)
    z = 1.0 / (torch.einsum("bnd,bd->bn", q_phi, k_phi.sum(dim=1)) + 1e-6)
    return torch.einsum("bnd,bde,bn->bne", q_phi, kv, z)


def grouped_query_attention(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    num_groups: int = 4,
) -> torch.Tensor:
    batch, seq_len, d_model = q.shape
    if d_model % num_groups != 0:
        raise ValueError(
            f"d_model ({d_model}) must be divisible by num_groups ({num_groups})."
        )

    group_dim = d_model // num_groups
    qg = q.view(batch, seq_len, num_groups, group_dim).permute(0, 2, 1, 3)
    k_shared = k.view(batch, seq_len, num_groups, group_dim).mean(dim=2)
    v_shared = v.view(batch, seq_len, num_groups, group_dim).mean(dim=2)

    outputs: list[torch.Tensor] = []
    for g in range(num_groups):
        scores = torch.matmul(qg[:, g], k_shared.transpose(-2, -1)) / math.sqrt(
            group_dim
        )
        weights = torch.softmax(scores, dim=-1)
        outputs.append(torch.matmul(weights, v_shared))

    out = torch.stack(outputs, dim=1).permute(0, 2, 1, 3)
    return out.reshape(batch, seq_len, d_model)


def timed_run(device: torch.device, fn, *args):
    if device.type == "cuda":
        torch.cuda.synchronize()
    start = time.perf_counter()
    out = fn(*args)
    if device.type == "cuda":
        torch.cuda.synchronize()
    return out, (time.perf_counter() - start) * 1000.0


def run_pipeline() -> dict[str, object]:
    exp_cfg = ExperimentConfig()

    torch.manual_seed(exp_cfg.seed)
    np.random.seed(exp_cfg.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(exp_cfg.seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    device = resolve_device()
    prep_cfg = PreprocessingConfig(
        num_samples=exp_cfg.num_samples,
        seq_len=exp_cfg.seq_len,
        max_vocab_size=4096,
        train_ratio=0.8,
    )
    data = prepare_text_data(prep_cfg, seed=exp_cfg.seed)

    embedding = torch.nn.Embedding(len(data.vocab), exp_cfg.d_model, device=device)
    with torch.no_grad():
        embedding.weight.copy_(
            torch.randn(len(data.vocab), exp_cfg.d_model, device=device) * 0.2
        )

    x_train = embedding(
        torch.tensor(data.train_token_ids, dtype=torch.long, device=device)
    )
    x_test = embedding(
        torch.tensor(data.test_token_ids, dtype=torch.long, device=device)
    )

    w_q, w_k, w_v = init_projection_weights(exp_cfg.d_model, device)
    q_train, k_train, v_train = apply_qkv_projection(x_train, w_q, w_k, w_v)
    q_test, k_test, v_test = apply_qkv_projection(x_test, w_q, w_k, w_v)

    teacher_train = dense_attention(q_train, k_train, v_train)
    temp_grid = torch.linspace(0.5, 2.0, exp_cfg.temperature_grid_size, device=device)

    best_temp = float(temp_grid[0].item())
    best_mse = float("inf")
    for temp in temp_grid:
        student = sparse_with_temperature(
            q_train,
            k_train,
            v_train,
            exp_cfg.local_window,
            float(temp.item()),
        )
        mse = float(torch.mean((student - teacher_train) ** 2).item())
        if mse < best_mse:
            best_mse = mse
            best_temp = float(temp.item())

    teacher_test, t_dense = timed_run(device, dense_attention, q_test, k_test, v_test)
    sparse_test, t_sparse = timed_run(
        device,
        sparse_with_temperature,
        q_test,
        k_test,
        v_test,
        exp_cfg.local_window,
        best_temp,
    )
    linear_test, t_linear = timed_run(device, linear_attention, q_test, k_test, v_test)
    gqa_test, t_gqa = timed_run(device, grouped_query_attention, q_test, k_test, v_test)

    return {
        "device": str(device),
        "best_temperature": best_temp,
        "dense_ms": float(t_dense),
        "sparse_ms": float(t_sparse),
        "linear_ms": float(t_linear),
        "gqa_ms": float(t_gqa),
        "sparse_mse_vs_dense": float(
            torch.mean((sparse_test - teacher_test) ** 2).item()
        ),
        "linear_mse_vs_dense": float(
            torch.mean((linear_test - teacher_test) ** 2).item()
        ),
        "gqa_mse_vs_dense": float(torch.mean((gqa_test - teacher_test) ** 2).item()),
    }


def main() -> None:
    metrics = run_pipeline()
    print({"library": "pytorch", "variant": "advanced", **metrics})


if __name__ == "__main__":
    main()
