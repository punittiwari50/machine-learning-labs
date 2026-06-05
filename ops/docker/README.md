# Docker Compose Stacks for Local Model Families

This folder contains one Docker Compose file per model family.

## Files

- `docker-compose.gemma.yml`
- `docker-compose.deepseek.yml`
- `docker-compose.qwen.yml`

## Shared Docker Network (Required)

All model containers and the MCP container must run on the same Docker network
so the MCP service can resolve model containers by name.

Create it once on host Windows PowerShell:

```powershell
docker network create mcp_model_net
```

If the network already exists, Docker returns an "already exists" message and
you can continue.

## Manual Run Pattern

Run from host Windows PowerShell.

### Gemma

```powershell
docker compose -f ops/docker/docker-compose.gemma.yml up -d
docker exec -it ollama-gemma ollama pull gemma3:latest
docker exec -it ollama-gemma ollama run gemma3:latest "Hello"
```

### DeepSeek

```powershell
docker compose -f ops/docker/docker-compose.deepseek.yml up -d
docker exec -it ollama-deepseek ollama pull deepseek-r1:latest
docker exec -it ollama-deepseek ollama run deepseek-r1:latest "Hello"
```

### Qwen

```powershell
docker compose -f ops/docker/docker-compose.qwen.yml up -d
docker exec -it ollama-qwen ollama pull qwen3:latest
docker exec -it ollama-qwen ollama run qwen3:latest "Hello"
```

## MCP Router (Single Container)

```powershell
docker compose -f model-router-mcp/docker-compose.yml up -d --build
```

MCP API endpoint:

- `http://localhost:8088/mcp`

Connectivity check from MCP container:

```powershell
docker exec model-router-mcp python -c "from model_router_mcp.config import AppConfig; from model_router_mcp.services.router import ModelRouter; s=ModelRouter(AppConfig.from_env()).status(); print({k:v.reachable for k,v in s.items()})"
```

Expected: `gemma`, `deepseek`, `qwen` should be `True` when all model
containers are healthy.

## Test From VS Code

1. Open `.vscode/mcp.json` and confirm:

```json
{
	"servers": {
		"model-router-mcp": {
			"type": "http",
			"url": "http://localhost:8088/mcp"
		}
	}
}
```

2. Run `MCP: List Servers` from Command Palette.
3. Start or restart `model-router-mcp`.
4. In Chat, call a tool-backed prompt such as:
	 - `Use model-router-mcp get_backend_status`
	 - `Use model-router-mcp ask_model with model='gemma' and prompt='hello'`

If VS Code shows an MCP error, open MCP server output and verify container
status with `docker ps` and endpoint reachability with
`curl http://localhost:8088/health`.

If `mcp.json` appears in error state but has valid schema, this is usually a
runtime issue (MCP container down, endpoint unreachable, or backend container
failed to boot).

## Shutdown

```powershell
docker compose -f ops/docker/docker-compose.gemma.yml down
docker compose -f ops/docker/docker-compose.deepseek.yml down
docker compose -f ops/docker/docker-compose.qwen.yml down
```
