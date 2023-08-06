import os
from dataclasses import dataclass


script_dir = os.path.dirname(__file__)
rel_path = "resources/tasks.json"
f = os.path.join(script_dir, rel_path)


@dataclass
class AppConfig:
    """Application Config."""

    API_PREFIX: str = os.getenv("API_PREFIX", "/wazuh")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 5002))
    PROJECT_NAME: str = "WAZUH API REST"
