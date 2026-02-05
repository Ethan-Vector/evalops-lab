from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


@dataclass
class MockProvider:
    id: str = "mock"

    def complete(self, prompt: str, meta: dict[str, Any] | None = None) -> str:
        # Deterministic, good enough for smoke + CI. Not meant to be smart.
        p = prompt.strip().lower()

        # Simple arithmetic extraction (e.g., "19*7")
        m = re.fullmatch(r"\s*(\d+)\s*([+\-*/])\s*(\d+)\s*", p)
        if m:
            a = int(m.group(1))
            op = m.group(2)
            b = int(m.group(3))
            if op == "+":
                return str(a + b)
            if op == "-":
                return str(a - b)
            if op == "*":
                return str(a * b)
            if op == "/":
                return str(a // b) if b != 0 else "division_by_zero"
        if "capital of italy" in p or "capitale d'italia" in p:
            return "Rome"
        if "two plus two" in p or "2+2" in p:
            return "4"
        if "hello" in p:
            return "Hello!"
        # fallback
        return f"MOCK_RESPONSE: {prompt[:120]}"
