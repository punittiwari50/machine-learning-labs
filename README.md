# machine-learning-labs
Machine learning with 

## Topic Modules

### Self-Attention Variants

- Overview: `self-attention-variants/README.md`
- Basic concepts: `self-attention-variants/basic.md`
- Basic code notebook: `self-attention-variants/basic.ipynb`
- Advanced concepts: `self-attention-variants/advanced.md`
- Advanced code notebook: `self-attention-variants/advanced.ipynb`

### Vulnerability Defenses

- Overview: `vulnerability-defenses/README.md`
- Input validation and sanitization: `vulnerability-defenses/input-validation-sanitization.md`
- Authentication and authorization hardening: `vulnerability-defenses/authn-authz-hardening.md`
- Secret and data protection: `vulnerability-defenses/secret-data-protection.md`
- Dependency and supply chain protection: `vulnerability-defenses/dependency-supply-chain-protection.md`
- Runtime and infrastructure hardening: `vulnerability-defenses/runtime-infrastructure-hardening.md`
- Monitoring and response readiness: `vulnerability-defenses/monitoring-response-readiness.md`

### Model Container Compatibility

- Overview: `model-container-compatibility/README.md`
- Docker compose ops: `ops/docker/README.md`
- Gemma latest: `model-container-compatibility/gemma-latest-docker.md`
- DeepSeek latest: `model-container-compatibility/deepseek-latest-docker.md`
- Qwen latest: `model-container-compatibility/qwen-latest-docker.md`

### Model Router MCP

- Project: `model-router-mcp/README.md`
- Docker Compose: `model-router-mcp/docker-compose.yml`
- VS Code MCP config: `.vscode/mcp.json`

MCP uses one Docker container and HTTP endpoint `http://localhost:8088/mcp`.
All model containers and MCP must join shared Docker network `mcp_model_net`.

## Local-Only Prompt Checks

Use these commands to verify responses are coming from local model containers
only (no Copilot model path):

```powershell
docker exec ollama-gemma ollama run gemma3:latest "Reply only: LOCAL_OK_GEMMA"
docker exec ollama-deepseek ollama run deepseek-r1:latest "Reply only: LOCAL_OK_DEEPSEEK"
docker exec ollama-qwen ollama run qwen3:latest "Reply only: LOCAL_OK_QWEN"
```

Latest model refresh commands:

```powershell
docker exec ollama-gemma ollama pull gemma3:latest
docker exec ollama-deepseek ollama pull deepseek-r1:latest
docker exec ollama-qwen ollama pull qwen3:latest
```

## Local MCP First (No Copilot First Go)

Use this flow when you want to communicate with local MCP directly and avoid
spending Copilot model tokens first.

1. Start local stacks only:

```powershell
docker compose -f ops/docker/docker-compose.gemma.yml up -d
docker compose -f ops/docker/docker-compose.deepseek.yml up -d
docker compose -f ops/docker/docker-compose.qwen.yml up -d
docker compose -f model-router-mcp/docker-compose.yml up -d --build
```

2. Verify local MCP is up:

```powershell
curl http://localhost:8088/mcp -H "Accept: text/event-stream"
```

3. Call local MCP tools without Copilot chat by using MCP Inspector:

```powershell
npx @modelcontextprotocol/inspector http://localhost:8088/mcp
```

4. In Inspector, run tools directly:
- `get_backend_status`
- `ask_model` with `model=gemma|deepseek|qwen`

5. Optional direct container checks (still local-only):

```powershell
docker exec ollama-gemma ollama run gemma3:latest "Reply only: LOCAL_OK_GEMMA"
docker exec ollama-deepseek ollama run deepseek-r1:latest "Reply only: LOCAL_OK_DEEPSEEK"
docker exec ollama-qwen ollama run qwen3:latest "Reply only: LOCAL_OK_QWEN"
```

6. VS Code Chat single-command local mode:

- Use slash command: `/local-mcp-only <your prompt>`
- Example: `/local-mcp-only Explain vector databases in 5 bullets`

Behavior:

- Calls local `model-router-mcp` only.
- Uses reachable model in order `gemma -> deepseek -> qwen`.
- Returns `LOCAL_MCP_UNAVAILABLE: start local containers and retry.` when local MCP is unavailable.

## Runtime Device Config

Use the project-level runtime flag file to switch GPU/CPU behavior:

- Template: `configs/runtime.env.example`
- Active config: `configs/runtime.env`
- `USE_GPU=1` => GPU mode (default)
- `USE_GPU=0` => CPU fallback

Foundation and PEFT notebooks automatically load `configs/runtime.env` (fallback: `configs/runtime.env.example`) and map `USE_GPU` to runtime device selection.

Quick switch:

1. Open `configs/runtime.env`
2. Set `USE_GPU=1` for GPU-first mode or `USE_GPU=0` to force CPU
3. Re-run the notebook from the first code cell
