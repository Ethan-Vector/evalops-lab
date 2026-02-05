# Adding tasks and datasets

## Dataset format (JSONL)

Each line is a JSON object:

- `id` (string): stable identifier
- `input` (string): prompt or question
- `expected_contains` (list[str], optional): cheap correctness proxy
- `tags` (list[str], optional): grouping
- `meta` (object, optional): any extra info

Example:

```json
{"id":"rag:pricing","input":"What is the pricing tier?","expected_contains":["Pro","Enterprise"],"tags":["rag"],"meta":{"source":"docs/pricing.md"}}
```

## Suites (YAML)

Suites define:
- datasets
- metrics
- gates
- run settings (max_cases, seed, etc.)

See `evals/suites/default.yaml`.
