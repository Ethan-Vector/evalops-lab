FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -e ".[dev]"

# Default command: run the suite and write workspace artifacts
CMD ["evalops", "run", "--suite", "evals/suites/default.yaml", "--provider", "mock"]
