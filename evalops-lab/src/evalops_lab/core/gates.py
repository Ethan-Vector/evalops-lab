from __future__ import annotations

from typing import Any


def eval_gates(summary: dict[str, Any], gates: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    """Return (pass, details). Gates are intentionally simple and CI-friendly."""
    details: dict[str, Any] = {}
    ok = True

    min_pass_rate = float(gates.get("min_pass_rate", 0.0))
    pass_rate = float(summary.get("pass_rate", 0.0))
    g_ok = pass_rate >= min_pass_rate
    details["min_pass_rate"] = {"required": min_pass_rate, "actual": pass_rate, "ok": g_ok}
    ok = ok and g_ok

    max_p95_latency_ms = gates.get("max_p95_latency_ms")
    if max_p95_latency_ms is not None:
        required = float(max_p95_latency_ms)
        actual = float(summary.get("p95_latency_ms", 0.0))
        g_ok = actual <= required
        details["max_p95_latency_ms"] = {"required": required, "actual": actual, "ok": g_ok}
        ok = ok and g_ok

    max_failures = gates.get("max_failures")
    if max_failures is not None:
        required = int(max_failures)
        actual = int(summary.get("failed", 0))
        g_ok = actual <= required
        details["max_failures"] = {"required": required, "actual": actual, "ok": g_ok}
        ok = ok and g_ok

    return ok, details
