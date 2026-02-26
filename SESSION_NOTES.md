# GraphLoom - Session Notes

Use this file as a running log between work sessions.

## Entry Template

### YYYY-MM-DD
- Summary:
- Changes:
- Files touched:
- Tests run:
- Known issues:
- Next steps:

## Current

### 2026-02-26
- Summary: Removed external theme package dependency and dropped compatibility theme selector flags.
- Changes:
  - Removed compatibility theme selector handling from CLI/runtime path.
  - Kept profile-driven `elkSettings` as the single runtime style mechanism.
  - Updated CLI regression coverage for profile-first behavior.
  - Removed optional theme package dependency from `pyproject.toml`.
- Files touched:
  - `src/graphloom/theme.py`
  - `src/graphloom/builder.py`
  - `tests/test_theme.py`
  - `pyproject.toml`
  - `PROJECT_CONTEXT.md`
  - `SESSION_NOTES.md`
- Tests run:
  - Pending.
- Known issues: none.
- Next steps:
  - Keep `theme.py` limited to pure metric mapping helpers for migration use-cases only.

### 2026-02-26
- Summary: Added GraphAPI profile bundle adapter for deterministic `elkSettings` consumption.
- Changes:
  - Added `src/graphloom/profile.py` with:
    - `resolve_profile_elk_settings`
    - `build_canvas_from_profile_bundle`
    - `ResolvedProfileElkSettings`
  - Exported adapter APIs from `graphloom.__init__`.
  - Added adapter-focused tests covering validation and deterministic mapping.
  - Updated docs/context notes.
- Files touched:
  - `src/graphloom/profile.py`
  - `src/graphloom/__init__.py`
  - `tests/test_profile_adapter.py`
  - `README.md`
  - `PROJECT_CONTEXT.md`
  - `SESSION_NOTES.md`
- Tests run:
  - `./.venv/bin/python -m pytest -q` (75 passed)
- Known issues: none.
- Next steps:
  - Expand adapter tests with larger real-world profile bundles.

### 2026-02-25
- Summary: Added persistent project/session context documentation.
- Changes:
  - Introduced `PROJECT_CONTEXT.md`.
  - Introduced `SESSION_NOTES.md`.
- Files touched:
  - `PROJECT_CONTEXT.md`
  - `SESSION_NOTES.md`
- Tests run: not run (docs-only update).
- Known issues: none.
- Next steps:
  - Keep this log updated as schema/settings behavior evolves.
