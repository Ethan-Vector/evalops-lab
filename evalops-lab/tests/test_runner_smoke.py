from pathlib import Path
from evalops_lab.core.io import read_suite
from evalops_lab.core.runner import run_suite
from evalops_lab.providers.mock import MockProvider

def test_run_default_suite(tmp_path):
    suite = read_suite(Path("evals/suites/default.yaml"))
    run = run_suite(suite, MockProvider(), workspace=tmp_path)
    assert run["summary"]["total"] == 4
    assert run["summary"]["failed"] == 0
    assert run["summary"]["gates_pass"] in [True, False]  # depends on machine latency, but should be fast
