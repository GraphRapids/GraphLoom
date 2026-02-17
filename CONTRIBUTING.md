# Contributing to GraphLoom

Thanks for contributing.

## Development Setup

1. Create and activate a virtual environment.
   `python3 -m venv .venv`
   `. .venv/bin/activate`
2. Install the project in editable mode with dev dependencies.
   `pip install -e .[dev]`

## Run Tests

- Run the full test suite: `pytest -q`

## Pull Request Guidelines

1. Branch from `main`.
2. Keep changes focused and include tests when behavior changes.
3. Update docs for user-facing behavior changes.
4. Ensure required checks pass: `CI`, `Tests`, and `Gitleaks`.
5. Request review from CODEOWNERS.

## Commit Messages

Conventional commit style is preferred:
- `feat: ...`
- `fix: ...`
- `docs: ...`
- `test: ...`
- `chore: ...`

## Security Issues

Do not file public issues for vulnerabilities.
Follow `SECURITY.md` for private reporting.

## Release Expectations

- Versioning follows SemVer.
- Update `CHANGELOG.md` for user-visible changes.
- Follow `RELEASE.md` for tagged releases.
