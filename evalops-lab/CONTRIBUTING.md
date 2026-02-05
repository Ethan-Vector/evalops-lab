# Contributing

This repo is meant to be forked and adapted.

## Guidelines

- Keep eval artifacts reproducible (JSONL datasets, YAML suites, JSON baselines)
- Prefer simple metrics + explicit gates
- Add new providers behind an interface; keep CI offline-first

## Local checks

```bash
ruff check .
pytest
evalops run --suite evals/suites/default.yaml --provider mock
```
