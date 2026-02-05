from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class Suite:
    name: str
    datasets: list[Path]
    metrics: list[str]
    gates: dict[str, Any]
    max_cases: int | None = None
    seed: int = 0


def read_suite(path: Path) -> Suite:
    obj = yaml.safe_load(path.read_text(encoding="utf-8"))
    name = obj.get("name", path.stem)
    datasets = [Path(p) for p in obj["datasets"]]
    metrics = obj.get("metrics", ["contains_any", "latency_ms"])
    gates = obj.get("gates", {"min_pass_rate": 1.0})
    return Suite(
        name=name,
        datasets=datasets,
        metrics=metrics,
        gates=gates,
        max_cases=obj.get("max_cases"),
        seed=int(obj.get("seed", 0)),
    )


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows
