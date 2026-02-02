import asyncio
from evalops_lab.config import load_config
from evalops_lab.dataset import TaskCase, GoldenCase
from evalops_lab.engine import EvalEngine
from evalops_lab.runners.local_stub import LocalStubRunner

def test_engine_smoke(tmp_path):
    cfg_text = '''
grading: {pass_rate_threshold: 0.5}
reporting: {reports_dir: "reports", traces_dir: "traces"}
runner: {kind: "local_stub"}
'''
    p = tmp_path / "c.yaml"
    p.write_text(cfg_text)
    cfg = load_config(str(p))

    tasks = [
        TaskCase(id="a", input="reset password", meta={}),
        TaskCase(id="b", input="unknown policy", meta={}),
    ]
    golden = {
        "a": GoldenCase(id="a", expect={"contains":["reset email"]}, should_pass=True),
        "b": GoldenCase(id="b", expect={"refusal":True}, should_pass=True),
    }
    eng = EvalEngine(cfg=cfg, runner=LocalStubRunner())
    rep, _ = asyncio.run(eng.run(tasks, golden))
    assert rep.total == 2
    assert rep.passed >= 1
