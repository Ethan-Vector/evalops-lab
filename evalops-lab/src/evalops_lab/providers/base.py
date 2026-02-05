from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


class Provider(Protocol):
    id: str

    def complete(self, prompt: str, meta: dict[str, Any] | None = None) -> str:
        ...
