# Model Router MCP

This is a separate Python MCP project that runs in Docker on the host machine and routes requests to the local model containers already mentioned in this workspace.

## Connected Backends

- Gemma via Ollama on `11434`
- DeepSeek via Ollama on `11435`
- Qwen via Ollama on `11436`

## Project Layout

- `src/model_router_mcp/config.py` - environment-driven configuration
- `src/model_router_mcp/clients/` - HTTP clients and service adapters
- `src/model_router_mcp/services/router.py` - orchestration and routing
- `src/model_router_mcp/server.py` - MCP server entrypoint
- `tests/` - lightweight unit tests

## Docker Run

Start the local model containers first from `ops/docker/`.

Create the shared Docker network once:

```powershell
docker network create mcp_model_net
```

Deploy the MCP container:

```powershell
cd model-router-mcp
docker compose up -d --build
```

This starts one MCP container (`model-router-mcp`) that serves MCP over HTTP.

The container connects to model services through Docker DNS on the shared
network:

- `ollama-gemma:11434`
- `ollama-deepseek:11434`
- `ollama-qwen:11434`

## Local API Communication

The MCP endpoint is exposed from the same single container for local API-based
integrations.

- Base URL: `http://localhost:8088`
- Streamable HTTP path: `/mcp`

This allows local applications and VS Code to communicate with MCP over API.

## VS Code MCP Connection

The workspace MCP config points VS Code to `http://localhost:8088/mcp`.

To test in VS Code:

1. Run `MCP: List Servers`.
2. Start/restart `model-router-mcp`.
3. Send a chat request using MCP tools, for example:
	 - `Use model-router-mcp get_backend_status`
	 - `Use model-router-mcp ask_qwen with prompt='hello'`

If VS Code reports an MCP error in `mcp.json`, validate:

- `docker ps` shows `model-router-mcp` up on `8088`.
- `curl http://localhost:8088/health` returns HTTP 200 with JSON liveness data.
- `curl http://localhost:8088/mcp -H "Accept: text/event-stream"` reaches the
	MCP stream endpoint.

## Available MCP Tools

- `get_backend_status`
- `ask_gemma`
- `ask_deepseek`
- `ask_qwen`
- `ask_model` (generic selector: `gemma`, `deepseek`, `qwen`)

## Answer Payload Contract

All ask tools return a structured payload:

```json
{
	"selected_model_family": "ollama",
	"selected_model_name": "gemma3:latest",
	"response_text": "...",
	"token_usage": {
		"prompt_tokens": 120,
		"completion_tokens": 210,
		"total_tokens": 330
	}
}
```

Token usage values come from each backend API response when available.

## Notes

- The server uses container-to-container DNS on shared network `mcp_model_net`.
- Model communication is local-only and does not use API keys or tokens.
