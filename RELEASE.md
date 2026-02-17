# Release Process

This project uses Semantic Versioning (SemVer) and tagged GitHub releases.

## Versioning Policy

- `MAJOR` (`X.0.0`): Breaking API or behavior changes
- `MINOR` (`0.X.0`): Backward-compatible features
- `PATCH` (`0.0.X`): Backward-compatible fixes and documentation-only release notes updates

Tag format is `vX.Y.Z` (for example, `v0.2.1`).

## Release Checklist

1. Ensure `main` is green (`CI`, `Tests`, and `Gitleaks`).
2. Update `CHANGELOG.md`:
   - Move items from `Unreleased` to a new version section.
   - Add release date.
3. Bump `version` in `pyproject.toml`.
4. Commit release prep:
   - `git add CHANGELOG.md pyproject.toml`
   - `git commit -m "chore(release): vX.Y.Z"`
5. Create and push an annotated tag:
   - `git tag -a vX.Y.Z -m "vX.Y.Z"`
   - `git push origin vX.Y.Z`
6. The `Release` workflow creates a GitHub release automatically for that tag.

## Hotfixes

For urgent fixes, branch from the latest release tag, apply the fix, and release as the next patch version.
