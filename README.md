# ethan-evalops-lab

Uno starter repo **EvalOps**: regression tests + metriche + report + trace bundle.
Serve a completare un libro di AI Engineering perché trasforma “vibes” in **release gates**.

Cosa include:
- Dataset in JSONL (task cases + golden expectations)
- Runner pluggable:
  - `local_stub` (per demo/offline)
  - `http_chat` (chiama un endpoint tipo gateway `/v1/chat/completions`)
- Metriche base (exact match / contains / citation-recall)
- Report JSON + traces per ogni caso (riproducibilità)
- CLI `evalops` + FastAPI API

> Nota: nessuna dipendenza ML pesante. Puoi innestare un vero LLM via HTTP senza cambiare il framework.

---

## Quickstart

### 1) Setup
```bash
cp .env.example .env
cp configs/evalops.example.yaml configs/evalops.yaml

python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2) Run eval (CLI)
```bash
evalops run --config configs/evalops.yaml --dataset data/tasks.jsonl --golden data/golden.jsonl
```

Output:
- `reports/latest_report.json`
- `traces/<run_id>/<case_id>.json`

### 3) Run API
```bash
make dev
# http://localhost:8098/healthz
```

---

## Dataset format

### tasks.jsonl
Ogni riga:
- `id`
- `input` (string o dict)
- `meta` (route, tags, ecc.)

### golden.jsonl
Ogni riga:
- `id`
- `expect` (es. exact/contains/citations)
- `should_pass` (bool)

---

## Esempio “gateway mode” (integrazione con repo 1)

Nel config imposta:
- runner: `http_chat`
- url: `http://localhost:8080/v1/chat/completions`
- headers: `x-tenant-id`, `x-route`

In questo modo EvalOps diventa il **release gate** del proxy/gateway.

---

## License
MIT
