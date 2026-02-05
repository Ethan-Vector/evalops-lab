from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from evalops_lab.core.io import read_suite
from evalops_lab.core.runner import run_suite
from evalops_lab.core.baseline import write_baseline, compare_to_baseline
from evalops_lab.core.report import render_html_report
from evalops_lab.providers.registry import get_provider


def _p(s: str) -> None:
    print(s, flush=True)


def cmd_doctor(_: argparse.Namespace) -> int:
    _p("evalops doctor: OK")
    _p("Python package import: OK")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    suite = read_suite(Path(args.suite))
    provider = get_provider(args.provider, config_path=args.config)
    run = run_suite(suite, provider, workspace=Path("workspace"))
    out_path = Path(args.out) if args.out else Path("workspace/last_run.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(run, indent=2), encoding="utf-8")
    _p(f"Wrote run artifact: {out_path}")
    return 0


def cmd_baseline(args: argparse.Namespace) -> int:
    suite = read_suite(Path(args.suite))
    provider = get_provider(args.provider, config_path=args.config)
    run = run_suite(suite, provider, workspace=Path("workspace"))
    out = Path(args.out)
    write_baseline(run, out)
    _p(f"Wrote baseline: {out}")
    return 0


def cmd_compare(args: argparse.Namespace) -> int:
    run = json.loads(Path(args.run).read_text(encoding="utf-8"))
    baseline = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
    result = compare_to_baseline(run, baseline)
    _p(json.dumps(result["summary"], indent=2))
    if not result["summary"]["gates_pass"]:
        _p("Gates: FAIL")
        return 1
    _p("Gates: PASS")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    run = json.loads(Path(args.run).read_text(encoding="utf-8"))
    html = render_html_report(run)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    _p(f"Wrote report: {out}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="evalops", description="EvalOps Lab CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    doctor = sub.add_parser("doctor", help="Sanity checks")
    doctor.set_defaults(fn=cmd_doctor)

    run = sub.add_parser("run", help="Run a suite and write run.json")
    run.add_argument("--suite", required=True, help="Path to suite YAML")
    run.add_argument("--provider", required=True, help="Provider id (e.g., mock)")
    run.add_argument("--config", default=None, help="Optional provider config file")
    run.add_argument("--out", default=None, help="Output path (default: workspace/last_run.json)")
    run.set_defaults(fn=cmd_run)

    baseline = sub.add_parser("baseline", help="Run suite and write a baseline JSON")
    baseline.add_argument("--suite", required=True)
    baseline.add_argument("--provider", required=True)
    baseline.add_argument("--config", default=None)
    baseline.add_argument("--out", required=True)
    baseline.set_defaults(fn=cmd_baseline)

    compare = sub.add_parser("compare", help="Compare run.json to baseline and enforce gates")
    compare.add_argument("--run", required=True)
    compare.add_argument("--baseline", required=True)
    compare.set_defaults(fn=cmd_compare)

    report = sub.add_parser("report", help="Generate HTML report from run.json")
    report.add_argument("--run", required=True)
    report.add_argument("--out", required=True)
    report.set_defaults(fn=cmd_report)

    return p


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    rc = args.fn(args)
    raise SystemExit(rc)


if __name__ == "__main__":
    main()
