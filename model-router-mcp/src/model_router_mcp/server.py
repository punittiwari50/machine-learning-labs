from __future__ import annotations

from dataclasses import asdict
from os import environ

from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from model_router_mcp.config import AppConfig
from model_router_mcp.services.router import ModelRouter


def create_server(host: str = "127.0.0.1", port: int = 8000) -> FastMCP:
    """Create the MCP server and register tools."""

    config = AppConfig.from_env()
    router = ModelRouter(config)
    server = FastMCP(
        "model-router-mcp",
        host=host,
        port=port,
        streamable_http_path="/mcp",
        stateless_http=True,
    )

    @server.custom_route("/health", methods=["GET"], include_in_schema=False)
    async def health_check(_request: Request) -> Response:
        """Return a simple liveness payload for non-MCP HTTP checks."""

        return JSONResponse(
            {
                "status": "ok",
                "service": "model-router-mcp",
                "transport": "streamable-http",
                "mcp_path": "/mcp",
            }
        )

    @server.tool()
    def get_backend_status() -> dict[str, object]:
        """Return reachability details for every configured backend."""

        status = router.status()
        return {name: asdict(item) for name, item in status.items()}

    @server.tool()
    def ask_gemma(
        prompt: str,
        system_prompt: str | None = None,
    ) -> dict[str, object]:
        """Send a prompt to Gemma through the local Ollama container."""

        return asdict(
            router.ask_gemma(prompt=prompt, system_prompt=system_prompt)
        )

    @server.tool()
    def ask_deepseek(
        prompt: str,
        system_prompt: str | None = None,
    ) -> dict[str, object]:
        """Send a prompt to DeepSeek through the local Ollama container."""

        return asdict(
            router.ask_deepseek(prompt=prompt, system_prompt=system_prompt)
        )

    @server.tool()
    def ask_qwen(
        prompt: str,
        system_prompt: str | None = None,
    ) -> dict[str, object]:
        """Send a prompt to Qwen through the local Ollama container."""

        return asdict(
            router.ask_qwen(prompt=prompt, system_prompt=system_prompt)
        )

    @server.tool()
    def ask_model(
        model: str,
        prompt: str,
        system_prompt: str | None = None,
    ) -> dict[str, object]:
        """Send a prompt by model key and return model + token metadata."""

        return asdict(
            router.ask_by_model(
                model=model,
                prompt=prompt,
                system_prompt=system_prompt,
            )
        )

    return server


def main() -> None:
    """Entry point for Docker and local development."""

    transport = environ.get("MCP_TRANSPORT", "stdio").strip().lower()
    if transport not in {"stdio", "sse", "streamable-http"}:
        raise RuntimeError(
            "Invalid MCP_TRANSPORT value. "
            "Use one of: stdio, sse, streamable-http."
        )

    host = environ.get("MCP_HOST", "0.0.0.0")
    port_raw = environ.get("MCP_PORT", "8088")
    try:
        port = int(port_raw)
    except ValueError as exc:
        raise RuntimeError("MCP_PORT must be a valid integer.") from exc

    mount_path = environ.get("MCP_MOUNT_PATH")
    if mount_path == "":
        mount_path = None

    server = create_server(host=host, port=port)
    try:
        server.run(transport=transport, mount_path=mount_path)
    finally:
        pass


if __name__ == "__main__":
    main()
