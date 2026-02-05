# EvalOps Lab — step-by-step

This repo is designed to be used like a lab. You can run everything offline.

## 1) Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## 2) Sanity check

```bash
evalops doctor
```

## 3) Run the default suite

```bash
evalops run --suite evals/suites/default.yaml --provider mock
```

Outputs:
- `workspace/last_run.json` (main artifact)
- `workspace/runs/<timestamp>/run.json` (archived run)

## 4) Generate a baseline

```bash
evalops baseline --suite evals/suites/default.yaml --provider mock --out evals/baselines/default.baseline.json
```

## 5) Compare vs baseline

```bash
evalops compare --run workspace/last_run.json --baseline evals/baselines/default.baseline.json
```

The command exits with code:
- `0` if gates pass
- `1` if gates fail

This is intentionally CI-friendly.

## 6) Add a dataset case (JSONL)

Open `evals/datasets/smoke.jsonl` and add a line:

```json
{"id":"smoke:new_case","input":"What is 2+2?","expected_contains":["4"],"tags":["math"]}
```

Then rerun.

## 7) Add a metric or gate

Metrics live in `src/evalops_lab/core/metrics.py`.  
Gates live in `src/evalops_lab/core/gates.py`.

Docs:
- `docs/metrics.md`
- `docs/evalops_principles.md`

## 8) CI

This repo includes a minimal GitHub Actions workflow:
- ruff (lint)
- pytest
- smoke eval run
- compare vs baseline

See `.github/workflows/ci.yml`.
