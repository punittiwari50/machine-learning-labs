# Model Container Compatibility (Docker-Only)

## Scope

This module provides a Docker-only workflow to run and validate these model families independently:

- Gemma (latest)
- DeepSeek (latest)
- Qwen (latest)

All execution paths below are containerized. Manual steps are documented in each model file.

## Local System Configuration Audit (June 3, 2026)

Detected configuration:

- OS: Windows 11 Pro 64-bit (10.0.26200)
- WSL: Ubuntu (WSL2, default)
- CPU: Intel Core Ultra 9 275HX (24 cores)
- RAM: 31.4 GB
- GPU: NVIDIA GeForce RTX 5080 Laptop GPU
- GPU VRAM: 16303 MiB (~16 GB)
- NVIDIA Driver: 610.47
- CUDA UMD: 13.3
- Docker: Client/Server 29.5.2
- Docker runtime includes: nvidia
- Docker GPU passthrough: validated with nvidia/cuda:12.6.2-base-ubuntu22.04

## Compatibility Summary for This Machine

- Strong fit:
  - Gemma small/medium latest variants (for example 2B, 4B, 9B with quantization)
  - DeepSeek distilled latest variants up to ~14B class with quantization
  - Qwen latest variants up to ~14B class with quantization
- Conditional fit:
  - 20B to 32B class models may run only with aggressive quantization, lower context length, and slower throughput
- Not practical for local single 16 GB VRAM:
  - Full frontier 70B+ or very large MoE checkpoints without remote/distributed serving

## Preflight (Docker-Only)

Run from host Windows PowerShell:

```powershell
docker version
docker info --format "{{json .Runtimes}}"
docker run --rm --gpus all nvidia/cuda:12.6.2-base-ubuntu22.04 nvidia-smi
```

Expected: nvidia runtime is listed and container can read GPU.

## Individual Guides

- [Gemma latest](gemma-latest-docker.md)
- [DeepSeek latest](deepseek-latest-docker.md)
- [Qwen latest](qwen-latest-docker.md)

## Compose Stacks

- [Docker ops overview](../ops/docker/README.md)
- [Gemma compose](../ops/docker/docker-compose.gemma.yml)
- [DeepSeek compose](../ops/docker/docker-compose.deepseek.yml)
- [Qwen compose](../ops/docker/docker-compose.qwen.yml)

## Shared Network for MCP Routing

When using `model-router-mcp`, run all model containers and MCP container on the
same Docker network (`mcp_model_net`) so MCP can reach model APIs by container
DNS name.

## Notes on "Latest"

Latest model/image tags change over time. Each guide includes a "discover current latest" step before launch so the process stays correct without hardcoding stale versions.
