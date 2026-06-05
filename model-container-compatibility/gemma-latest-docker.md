# Gemma Latest - Docker Runbook

## 1) Compatibility to Local System

Your machine (RTX 5080 Laptop 16 GB VRAM, 31 GB RAM) is compatible with Gemma latest small/medium variants in containerized mode.

Recommended local target:

- Gemma <= 12B class with quantization
- Best throughput/latency balance typically at 2B to 9B class

## 2) Docker-Only Manual Steps

### Step A - Validate GPU from container

```powershell
docker run --rm --gpus all nvidia/cuda:12.6.2-base-ubuntu22.04 nvidia-smi
```

### Step B - Start Ollama in Docker

```powershell
docker volume create ollama_data
docker run -d --name ollama-gemma --restart unless-stopped --gpus all -p 11434:11434 -v ollama_data:/root/.ollama ollama/ollama:latest
```

### Step C - Discover and pull latest Gemma

```powershell
docker exec -it ollama-gemma ollama list
docker exec -it ollama-gemma ollama pull gemma3:latest
```

If your registry naming differs, inspect available Gemma model names and pull the latest published tag.

### Step D - Run inference test

```powershell
docker exec -it ollama-gemma ollama run gemma3:latest "Summarize why containerized model serving improves reproducibility."
```

### Step E - Throughput sanity check

```powershell
docker exec -it ollama-gemma ollama run gemma3:latest "Write 5 short bullet points on GPU memory optimization for LLM serving."
```

## 3) Decision

- Compatible: Yes
- Recommended for this machine: Yes
- Scale-up condition: move to multi-GPU or remote endpoint for very large Gemma variants

## 4) Live Validation Notes (2026-06-03)

Executed from Docker container:

- Compose up: success (`ops/docker/docker-compose.gemma.yml`)
- Model pull (`gemma3:latest`): 49.79s
- Warm inference run: 2.36s
- Prompt check: passed (`OK docker gpu reproducible`)

Benchmark interpretation:

- Gemma is operational on local RTX 5080 16 GB in containerized mode.
- Warm-start latency is low enough for local experimentation and dev workflows.
