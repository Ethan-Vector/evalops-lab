from __future__ import annotations

import json
import time
from dataclasses import asdict
from pathlib import Path
from statistics import median

from evalops_lab.core.io import Suite, read_jsonl
from evalops_lab.core.metrics import compute_case_metrics
from evalops_lab.core.gates import eval_gates
from evalops_lab.providers.base import Provider


def _p95(values: list[float]) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    idx = int(0.95 * (len(s) - 1))
    return float(s[idx])


def run_suite(suite: Suite, provider: Provider, workspace: Path) -> dict:
    workspace.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d-%H%M%S")
    run_dir = workspace / "runs" / ts
    run_dir.mkdir(parents=True, exist_ok=True)

    # Load cases
    cases = []
    for ds in suite.datasets:
        cases.extend(read_jsonl(ds))
    if suite.max_cases is not None:
        cases = cases[: suite.max_cases]

    results = []
    latencies = []
    passed = 0
    failed = 0

    for case in cases:
        t0 = time.perf_counter()
        output = provider.complete(case["input"], meta=case.get("meta", {}))
        t1 = time.perf_counter()
        latency_ms = (t1 - t0) * 1000.0
        latencies.append(latency_ms)

        cm = compute_case_metrics(case, output, latency_ms, suite.metrics)
        if cm.passed:
            passed += 1
        else:
            failed += 1

        results.append({
            "id": case.get("id"),
            "input": case.get("input"),
            "tags": case.get("tags", []),
            "output": output,
            "passed": cm.passed,
            "checks": cm.checks,
        })

    total = len(results)
    pass_rate = (passed / total) if total else 0.0

    summary = {
        "suite": suite.name,
        "provider": provider.id,
        "total": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": pass_rate,
        "median_latency_ms": float(median(latencies)) if latencies else 0.0,
        "p95_latency_ms": _p95(latencies),
    }

    gates_pass, gate_details = eval_gates(summary, suite.gates)
    summary["gates_pass"] = gates_pass
    summary["gate_details"] = gate_details

    run = {
        "version": 1,
        "timestamp": ts,
        "suite": asdict(suite) | {"datasets": [str(p) for p in suite.datasets]},
        "provider": {"id": provider.id},
        "summary": summary,
        "results": results,
    }

    (run_dir / "run.json").write_text(json.dumps(run, indent=2), encoding="utf-8")
    (workspace / "last_run.json").write_text(json.dumps(run, indent=2), encoding="utf-8")
    return run
