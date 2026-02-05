# CI/CD integration

This repo is intentionally CI-first.

## Recommended pipeline

1) Lint + unit tests  
2) Run eval suite(s)  
3) Compare to baseline and fail on regressions  
4) Upload run artifacts as build artifacts (optional)

## Why fail the build?

Because “we'll check later” becomes “we never check”.

If you need a softer rollout, gate only on smoke suites in PRs and run heavier suites nightly.
