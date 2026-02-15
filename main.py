"""Development convenience entrypoint.

Run:
    python main.py examples/example_01.yaml -s examples/example.settings.toml -o /tmp/elk.json
"""

from graphloom.builder import main as _builder_main


def main(argv: list[str] | None = None) -> int:
    return _builder_main(argv)

if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
