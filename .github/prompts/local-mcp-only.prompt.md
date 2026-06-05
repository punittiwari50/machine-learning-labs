---
description: "Use local model-router-mcp tools only (gemma/deepseek/qwen) and return no-tool-fallback error if MCP is unavailable"
agent: agent
argument-hint: "Prompt to send to local model (for example: explain retrieval-augmented generation in 5 bullets)"
tools: [mcp_model-router-_ask_model, mcp_model-router-_get_backend_status]
---

You are in strict local MCP mode.

## Mission

Execute the user request by calling only the local `model-router-mcp` tools.

## Required Execution Order

1. Call `mcp_model-router-_get_backend_status` first.
2. Select the first reachable model in this order: `gemma`, `deepseek`, `qwen`.
3. Call `mcp_model-router-_ask_model` with:
   - `model`: selected model key from step 2.
   - `prompt`: exactly the user argument text.
4. Return the tool response content.

## Hard Constraints

- Do not answer from Copilot-native reasoning if MCP tools fail.
- Do not use any non-local model route.
- Do not call multimodal or removed model routes.
- If no local model is reachable, return exactly:
  `LOCAL_MCP_UNAVAILABLE: start local containers and retry.`

## Output Contract

Always include:

- `SOURCE: LOCAL_MCP`
- `MODEL_USED: <gemma|deepseek|qwen>`
- `MCP_SERVER: model-router-mcp`

If unavailable, include:

- `SOURCE: LOCAL_MCP`
- `MODEL_USED: none`
- `MCP_SERVER: model-router-mcp`
- `LOCAL_MCP_UNAVAILABLE: start local containers and retry.`
