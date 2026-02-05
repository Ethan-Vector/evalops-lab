# Metrics

This repo ships with a few pragmatic metrics:

- `contains_any`: expected substrings appear in the output
- `exact_match`: strict string match (use sparingly)
- `latency_ms`: measured per case (provider side)
- `pass_rate`: aggregate metric across cases

## Designing good metrics

- Prefer metrics that correlate with user-visible correctness
- Use `contains_any` as a fast smoke check, not as a final judge
- Add task-specific checks for critical flows (IDs, JSON validity, citations, etc.)

## Where to add metrics

See `src/evalops_lab/core/metrics.py`.
