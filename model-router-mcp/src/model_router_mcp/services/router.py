from __future__ import annotations

from collections.abc import Callable

from model_router_mcp.clients.ollama_client import OllamaClient
from model_router_mcp.config import AppConfig
from model_router_mcp.models import BackendStatus
from model_router_mcp.models import RoutedResponse


class ModelRouter:
    """Application service that routes calls to the configured backends."""

    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._gemma = OllamaClient(
            config.gemma.base_url,
            config.gemma.model_name,
            config.request_timeout_seconds,
        )
        self._deepseek = OllamaClient(
            config.deepseek.base_url,
            config.deepseek.model_name,
            config.request_timeout_seconds,
        )
        self._qwen = OllamaClient(
            config.qwen.base_url,
            config.qwen.model_name,
            config.request_timeout_seconds,
        )

    def ask_gemma(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> RoutedResponse:
        return self._gemma.generate(prompt=prompt, system_prompt=system_prompt)

    def ask_deepseek(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> RoutedResponse:
        return self._deepseek.generate(prompt=prompt, system_prompt=system_prompt)

    def ask_qwen(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> RoutedResponse:
        return self._qwen.generate(prompt=prompt, system_prompt=system_prompt)

    def ask_by_model(
        self,
        model: str,
        prompt: str,
        system_prompt: str | None = None,
    ) -> RoutedResponse:
        """Route a request by explicit model key."""

        normalized = model.strip().lower()
        if normalized == "gemma":
            return self.ask_gemma(prompt=prompt, system_prompt=system_prompt)
        if normalized == "deepseek":
            return self.ask_deepseek(prompt=prompt, system_prompt=system_prompt)
        if normalized == "qwen":
            return self.ask_qwen(prompt=prompt, system_prompt=system_prompt)

        raise ValueError(
            "Unsupported model. Use one of: "
            "gemma, deepseek, qwen."
        )

    def status(self) -> dict[str, BackendStatus]:
        return {
            "gemma": self._backend_status(
                "gemma",
                self._config.gemma.base_url,
                self._gemma.health_check,
            ),
            "deepseek": self._backend_status(
                "deepseek",
                self._config.deepseek.base_url,
                self._deepseek.health_check,
            ),
            "qwen": self._backend_status(
                "qwen",
                self._config.qwen.base_url,
                self._qwen.health_check,
            ),
        }

    def close(self) -> None:
        self._gemma.close()
        self._deepseek.close()
        self._qwen.close()

    @staticmethod
    def _backend_status(
        name: str,
        base_url: str,
        callback: Callable[[], object],
    ) -> BackendStatus:
        try:
            payload = callback()
            return BackendStatus(
                name=name,
                base_url=base_url,
                reachable=True,
                detail=str(payload),
            )
        except Exception as exc:  # noqa: BLE001
            return BackendStatus(
                name=name,
                base_url=base_url,
                reachable=False,
                detail=str(exc),
            )
