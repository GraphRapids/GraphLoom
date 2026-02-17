# Third-Party Notices

Last verified: 2026-02-17

GraphLoom is licensed under Apache-2.0. This file documents third-party software and tools used by the project.

## Runtime dependencies

| Component | How GraphLoom uses it | License | Source |
| --- | --- | --- | --- |
| `pydantic` | Data models and validation | MIT | https://github.com/pydantic/pydantic |
| `pydantic-settings` | Settings loading and environment overrides | MIT | https://github.com/pydantic/pydantic-settings |
| `PyYAML` | YAML input parsing | MIT | https://github.com/yaml/pyyaml |
| `tomli` (Python < 3.11) | TOML parsing fallback | MIT | https://github.com/hukkin/tomli |

## Optional layout runtime (not redistributed)

| Component | How GraphLoom uses it | License | Source |
| --- | --- | --- | --- |
| Eclipse Layout Kernel (ELK) | Graph layout model and options reference | EPL-2.0 | https://github.com/eclipse-elk/elk |
| `elkjs` | Optional local layout execution via Node.js | EPL-2.0 | https://github.com/kieler/elkjs |
| Node.js / npm | Optional runtime for `--layout` modes | Mixed (Node.js project licensing) | https://nodejs.org/ |

## Build and development tooling (not redistributed)

| Component | How GraphLoom uses it | License | Source |
| --- | --- | --- | --- |
| `setuptools` | Build backend (`setuptools.build_meta`) | MIT | https://github.com/pypa/setuptools |
| `wheel` | Wheel artifact creation | MIT | https://github.com/pypa/wheel |
| `pytest` | Test framework | MIT | https://github.com/pytest-dev/pytest |

## Downstream obligations

- If you enable `--layout`, ensure your distribution and compliance process includes `elkjs`/Node.js obligations in your environment.
- Keep this file updated when runtime dependencies, build tooling, or optional integrations change.

## Verification sources used for this update

- Local project files:
  - `pyproject.toml`
  - `README.md`
  - `src/graphloom/builder.py`
  - `src/graphloom/elkjs.py`
- Upstream repositories and package metadata linked above.
