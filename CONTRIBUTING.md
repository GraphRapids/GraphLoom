# Contributing

Thanks for contributing to GraphLoom.

## Development Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Running Checks

Run tests:

```bash
python -m pytest -q
```

Run a CLI smoke check:

```bash
python -m graphloom.builder examples/example_01.yaml -s examples/example.settings.toml -o /tmp/graphloom-check.json
```

## Project Structure

- `src/graphloom/`: library code
- `main.py`: local development entrypoint
- `tests/`: pytest suite
- `examples/`: sample minimal inputs and settings
- `.github/workflows/`: CI, tests, release, and secret scanning

## Pull Requests

Before opening a PR:

1. Keep changes focused and atomic.
2. Add or update tests for behavioral changes.
3. Update docs (`README.md`, `CHANGELOG.md`, `THIRD_PARTY_NOTICES.md`) when relevant.
4. Ensure workflows are green (`CI`, `Tests`, `Gitleaks`).

## Commit Guidance

- Use clear, imperative commit messages.
- Prefer conventional prefixes (`feat`, `fix`, `docs`, `test`, `chore`).
- Reference issue numbers when applicable.
- Avoid bundling unrelated changes in one PR.

## Reporting Bugs and Requesting Features

Use GitHub issue templates:

- Bug report
- Feature request

For security issues, follow `SECURITY.md`.
