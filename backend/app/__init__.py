from __future__ import annotations

import os

class Settings:
    app_name: str = "Personal AI Agent Trainer"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))

settings = Settings()
