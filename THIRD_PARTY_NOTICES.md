# Third-Party Notices

GraphLoom depends on third-party open source projects. This document provides
attribution and quick license references for projects used directly by this
repository.

This file is informational and does not replace the license terms of upstream
projects. See each project's repository and license file for the authoritative
license text.

## Runtime Dependencies

| Project | Purpose in GraphLoom | License | Source |
| --- | --- | --- | --- |
| Pydantic | Data models and validation | MIT | https://github.com/pydantic/pydantic |
| pydantic-settings | Settings loading and environment integration | MIT | https://github.com/pydantic/pydantic-settings |
| PyYAML | YAML input parsing | MIT | https://github.com/yaml/pyyaml |
| tomli | TOML parsing fallback on Python < 3.11 | MIT | https://github.com/hukkin/tomli |

## Optional Layout Runtime

| Project | Purpose in GraphLoom | License | Source |
| --- | --- | --- | --- |
| Eclipse Layout Kernel (ELK) | Graph layout engine and option model | EPL-2.0 | https://github.com/eclipse-elk/elk |
| elkjs | JavaScript/Node runtime binding for ELK layout | EPL-2.0 | https://github.com/kieler/elkjs |

## Development Dependencies

| Project | Purpose in GraphLoom | License | Source |
| --- | --- | --- | --- |
| pytest | Test framework | MIT | https://github.com/pytest-dev/pytest |
