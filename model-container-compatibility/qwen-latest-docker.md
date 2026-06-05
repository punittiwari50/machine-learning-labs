# Qwen Latest - Docker Runbook

## 1) Compatibility to Local System

Your machine is compatible with Qwen latest compact and mid-size variants under Docker with GPU.

Practical local target:

- Qwen <= 14B class with quantization for reliable local execution
- Larger checkpoints can become unstable or too slow on 16 GB VRAM

## 2) Docker-Only Manual Steps

### Step A - Validate GPU in Docker

```powershell
docker run --rm --gpus all nvidia/cuda:12.6.2-base-ubuntu22.04 nvidia-smi
```

### Step B - Run Ollama container for Qwen

```powershell
docker volume create ollama_data
docker run -d --name ollama-qwen --restart unless-stopped --gpus all -p 11436:11434 -v ollama_data:/root/.ollama ollama/ollama:latest
```

### Step C - Pull latest Qwen

```powershell
docker exec -it ollama-qwen ollama pull qwen3:latest
```

### Step D - Inference smoke test

```powershell
docker exec -it ollama-qwen ollama run qwen3:latest "Provide a 3-step MLOps rollback strategy."
```

### Step E - Verify stable serving loop

```powershell
docker exec -it ollama-qwen ollama run qwen3:latest "List 5 deployment guardrails for production LLM APIs."
```

## 3) Decision

- Compatible: Yes
- Recommended for this machine: Yes (small to medium Qwen variants)
- Caution: tune context length and batch size for higher parameter variants

## 4) Live Validation Notes (2026-06-03)

Executed from Docker container:

- Compose up: success (`ops/docker/docker-compose.qwen.yml`)
- Model pull (`qwen3:latest`): 68.44s
- First inference run: 40.03s
- Prompt check: model returned expected phrase but also prepended extended reasoning text

Benchmark interpretation:

- Qwen is operational in local Docker GPU mode.
- Initial response latency is in the same band as DeepSeek for this test prompt.
