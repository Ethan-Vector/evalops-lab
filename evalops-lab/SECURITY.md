# Security

This repository is a reference implementation.

- Do not commit API keys or secrets.
- Use `.env` locally and CI secrets in your pipeline.
- Treat prompts and datasets as potentially sensitive.

If you add network-capable tools/providers, add allowlists, timeouts, and request size limits.
