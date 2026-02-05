from __future__ import annotations

import copy
from pathlib import Path
from typing import Any


def write_baseline(run: dict[str, Any], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    baseline = {
        "version": 1,
        "suite": run.get("suite", {}).get("name", run.get("suite", {}).get("name")),
        "provider": run.get("provider", {}),
        "summary": run.get("summary") or run.get("summary"),
        "by_case": {r["id"]: {"passed": r["passed"], "checks": r["checks"]} for r in run["results"]},
        "meta": {"generated_from_run_timestamp": run.get("timestamp")},
    }
    # In case run format differs, normalize summary location
    if "summary" not in baseline or baseline["summary"] is None:
        baseline["summary"] = run.get("summary", {})
    out_path.write_text(__import__("json").dumps(baseline, indent=2), encoding="utf-8")


def compare_to_baseline(run: dict[str, Any], baseline: dict[str, Any]) -> dict[str, Any]:
    # Normalize
    run_summary = run.get("summary", run.get("summary", {})) or run.get("summary", {})
    base_summary = baseline.get("summary", {})

    diffs = []
    regressions = 0
    improvements = 0

    base_by_case = baseline.get("by_case", {})
    for r in run.get("results", []):
        cid = r.get("id")
        prev = base_by_case.get(cid)
        if prev is None:
            diffs.append({"id": cid, "change": "new_case", "passed": r.get("passed")})
            continue
        if bool(prev.get("passed")) != bool(r.get("passed")):
            change = "regression" if prev.get("passed") and (not r.get("passed")) else "improvement"
            if change == "regression":
                regressions += 1
            else:
                improvements += 1
            diffs.append({"id": cid, "change": change, "before": prev.get("passed"), "after": r.get("passed")})

    # Gate evaluation: prefer run's own computed gates
    gates_pass = bool(run_summary.get("gates_pass", False))
    gate_details = run_summary.get("gate_details", {})

    summary = {
        "gates_pass": gates_pass,
        "regressions": regressions,
        "improvements": improvements,
        "total_cases": int(run_summary.get("total", 0)),
        "pass_rate": float(run_summary.get("pass_rate", 0.0)),
        "p95_latency_ms": float(run_summary.get("p95_latency_ms", 0.0)),
        "gate_details": gate_details,
    }

    return {"summary": summary, "diffs": diffs}
