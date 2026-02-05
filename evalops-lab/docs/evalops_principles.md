# EvalOps principles

EvalOps = evaluation + operations.

If your model behavior changes and you can't:
- detect it,
- reproduce it,
- explain it,
- and gate releases on it,

then you're not operating the system — you're hoping.

## The core loop

1. Define datasets as versioned artifacts (`evals/datasets/*.jsonl`)
2. Run suites in a deterministic environment (CI-friendly)
3. Produce a run artifact (`run.json`)
4. Compare to a baseline + enforce gates
5. Ship only when gates pass
6. When you intentionally change behavior, update the baseline with a documented reason

## Why baselines matter

A baseline is not “truth”. It's a **contract**:
- this is what we shipped last time
- this is what we promise users today
- this is the budget we accept (quality/latency/cost)

## Common failure modes

- “One-off eval scripts” not wired to CI
- No baseline, only “scores”
- Datasets that drift without versioning
- Metrics that don't map to user value
- Gates that are too strict (block product) or too weak (allow regressions)

This repo keeps it deliberately simple so you can adapt it quickly.
