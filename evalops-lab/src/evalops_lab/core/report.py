from __future__ import annotations

import html
from typing import Any


def render_html_report(run: dict[str, Any]) -> str:
    summary = run.get("summary", {})
    rows = []
    for r in run.get("results", []):
        status = "PASS" if r.get("passed") else "FAIL"
        rows.append(
            f"<tr><td>{html.escape(str(r.get('id')))}</td>"
            f"<td>{status}</td>"
            f"<td><pre style='white-space:pre-wrap'>{html.escape(r.get('input',''))}</pre></td>"
            f"<td><pre style='white-space:pre-wrap'>{html.escape(r.get('output',''))}</pre></td></tr>"
        )

    gates = summary.get("gate_details", {})
    gate_lines = []
    for k, v in gates.items():
        gate_lines.append(f"<li><b>{html.escape(k)}</b>: {html.escape(str(v))}</li>")

    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>EvalOps Report - {html.escape(str(summary.get('suite','suite')))}</title>
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial; margin: 24px; }}
    .card {{ border: 1px solid #ddd; border-radius: 12px; padding: 16px; margin-bottom: 16px; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ border-bottom: 1px solid #eee; padding: 8px; vertical-align: top; }}
    th {{ text-align: left; }}
    pre {{ margin: 0; }}
    .pill {{ display: inline-block; padding: 2px 10px; border-radius: 999px; border: 1px solid #ddd; }}
  </style>
</head>
<body>
  <h1>EvalOps Report</h1>

  <div class="card">
    <div><span class="pill">suite: {html.escape(str(summary.get('suite')))}</span>
         <span class="pill">provider: {html.escape(str(run.get('provider',{}).get('id')))}</span>
         <span class="pill">timestamp: {html.escape(str(run.get('timestamp')))}</span></div>
    <p><b>pass_rate</b>: {summary.get('pass_rate')}</p>
    <p><b>p95_latency_ms</b>: {summary.get('p95_latency_ms')}</p>
    <p><b>gates_pass</b>: {summary.get('gates_pass')}</p>
    <h3>Gate details</h3>
    <ul>
      {''.join(gate_lines) if gate_lines else '<li>(none)</li>'}
    </ul>
  </div>

  <div class="card">
    <h2>Cases</h2>
    <table>
      <thead><tr><th>ID</th><th>Status</th><th>Input</th><th>Output</th></tr></thead>
      <tbody>
        {''.join(rows)}
      </tbody>
    </table>
  </div>
</body>
</html>"""
