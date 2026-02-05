from __future__ import annotations

from pathlib import Path

from evalops_lab.core.io import read_suite
from evalops_lab.core.runner import run_suite
from evalops_lab.providers.registry import get_provider


def main() -> None:
    suite = read_suite(Path("evals/suites/default.yaml"))
    provider = get_provider("mock")
    run_suite(suite, provider, workspace=Path("workspace"))


if __name__ == "__main__":
    main()
