# DeepSeek Latest - Docker Runbook

## 1) Compatibility to Local System

Your machine is compatible with latest DeepSeek distilled local variants (for example 7B/8B/14B class with quantization).

Practical local guidance:

- Use distilled/compact DeepSeek variants for smooth local serving
- Avoid full ultra-large checkpoints on single 16 GB VRAM

## 2) Docker-Only Manual Steps

### Step A - Validate GPU runtime

```powershell
docker run --rm --gpus all nvidia/cuda:12.6.2-base-ubuntu22.04 nvidia-smi
```

### Step B - Start Ollama container

```powershell
docker volume create ollama_data
docker run -d --name ollama-deepseek --restart unless-stopped --gpus all -p 11435:11434 -v ollama_data:/root/.ollama ollama/ollama:latest
```

### Step C - Pull latest DeepSeek model

```powershell
docker exec -it ollama-deepseek ollama pull deepseek-r1:latest
```

If your local model registry exposes a different DeepSeek latest tag, use that exact name.

### Step D - Validate response generation

```powershell
docker exec -it ollama-deepseek ollama run deepseek-r1:latest "Explain the difference between latency and throughput for LLM inference."
```

### Step E - Observe memory pressure

```powershell
docker stats --no-stream ollama-deepseek
```

## 3) Decision

- Compatible: Yes (distilled/smaller DeepSeek variants)
- Recommended for this machine: Yes
- Not recommended locally: very large DeepSeek checkpoints requiring much higher VRAM

## 4) Live Validation Notes (2026-06-03)

Executed from Docker container:

- Compose up: success (`ops/docker/docker-compose.deepseek.yml`)
- Model pull (`deepseek-r1:latest`): 65.63s
- First inference run: 43.42s
- Prompt check: model generated a valid response, but it ignored the exact-output constraint and produced extended reasoning text

Benchmark interpretation:

- DeepSeek runs successfully in container on this machine.
- First-token and first-response latency are much higher than Gemma in this setup.
