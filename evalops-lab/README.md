# evalops-lab

**EvalOps Lab** is a small, *offline-first* lab to design, run, baseline, compare, and gate **LLM / RAG evaluations** in CI.

It’s built around one idea: **Evals are a release artifact.**  
If you can’t reproduce them, diff them, and fail a build on regressions, you don’t really “have evals”.

## What you get

- A **suite format** (YAML) to define datasets, provider, metrics, and pass/fail gates
- An **eval runner** that produces a single `run.json` with per-case details + summary
- A **baseline system** to store known-good results and compare new runs
- A **report generator** (HTML) for quick human inspection
- A deterministic **Mock provider** (no API keys) so CI always works
- GitHub Actions CI (lint + tests + smoke eval + gate)

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
evalops doctor
evalops run --suite evals/suites/default.yaml --provider mock
evalops report --run workspace/last_run.json --out workspace/report.html
```

## Typical workflow (real life)

1. Write / extend datasets in `evals/datasets/*.jsonl`
2. Define a suite in `evals/suites/*.yaml`
3. Generate a baseline:
   ```bash
   evalops baseline --suite evals/suites/default.yaml --provider mock --out evals/baselines/default.baseline.json
   ```
4. In CI, run + compare:
   ```bash
   evalops run --suite evals/suites/default.yaml --provider mock
   evalops compare --run workspace/last_run.json --baseline evals/baselines/default.baseline.json
   ```

## Repo layout

- `src/evalops_lab/` → the library + CLI
- `evals/` → datasets, suites, baselines
- `docs/` → principles + how-to
- `tests/` → unit + smoke
- `.github/workflows/ci.yml` → CI pipeline

## Notes

- This repo ships with a **Mock** provider.  
  Add real providers (OpenAI / Azure / Anthropic / local vLLM) by implementing the `Provider` protocol in `src/evalops_lab/providers/`.

See `INSTRUCTIONS.md` for a step-by-step walkthrough.
