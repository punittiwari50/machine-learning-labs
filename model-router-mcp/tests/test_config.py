import sys
import unittest
from pathlib import Path

PROJECT_SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(PROJECT_SRC))

from model_router_mcp.config import AppConfig


class AppConfigTests(unittest.TestCase):
    def test_defaults_include_host_docker_internal_endpoints(self) -> None:
        config = AppConfig.from_env()
        self.assertIn("host.docker.internal", config.gemma.base_url)
        self.assertEqual(config.gemma.model_name, "gemma3:latest")
        self.assertEqual(config.deepseek.model_name, "deepseek-r1:latest")
        self.assertEqual(config.qwen.model_name, "qwen3:latest")
