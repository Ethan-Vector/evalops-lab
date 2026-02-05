from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class CaseMetrics:
    passed: bool
    checks: dict[str, Any]


def contains_any(output: str, expected: list[str] | None) -> tuple[bool, dict[str, Any]]:
    if not expected:
        return True, {"reason": "no_expected_contains"}
    hits = [s for s in expected if s in output]
    return (len(hits) > 0), {"expected": expected, "hits": hits}


def exact_match(output: str, expected: str | None) -> tuple[bool, dict[str, Any]]:
    if expected is None:
        return True, {"reason": "no_expected_exact"}
    ok = output.strip() == expected.strip()
    return ok, {"expected": expected, "output": output}


def compute_case_metrics(case: dict[str, Any], output: str, latency_ms: float, metrics: list[str]) -> CaseMetrics:
    checks: dict[str, Any] = {}
    passed = True

    if "contains_any" in metrics:
        ok, info = contains_any(output, case.get("expected_contains"))
        checks["contains_any"] = {"ok": ok, **info}
        passed = passed and ok

    if "exact_match" in metrics:
        ok, info = exact_match(output, case.get("expected_exact"))
        checks["exact_match"] = {"ok": ok, **info}
        passed = passed and ok

    if "latency_ms" in metrics:
        checks["latency_ms"] = {"value": float(latency_ms)}

    if "output_len" in metrics:
        checks["output_len"] = {"value": len(output)}

    return CaseMetrics(passed=passed, checks=checks)
