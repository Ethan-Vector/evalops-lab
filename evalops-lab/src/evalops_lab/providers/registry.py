from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from evalops_lab.providers.mock import MockProvider


def get_provider(provider_id: str, config_path: str | None = None):
    provider_id = provider_id.strip().lower()
    if provider_id == "mock":
        return MockProvider()

    # Placeholders for real providers; keep repo self-contained and safe.
    raise ValueError(
        f"Unknown provider '{provider_id}'. This repo ships only with 'mock'. "
        "Add your provider in src/evalops_lab/providers/ and register it here."
    )
