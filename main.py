"""Example entrypoint: enrich minimal graph JSON/YAML into ELK JSON.

Run:
    python main.py -i examples/example_01.yaml -s examples/example.settings.toml -o /tmp/elk.json
"""

import argparse
import json
from pathlib import Path

from elkpydantic.builder import build_canvas, _load_input, _load_settings
from elkpydantic.settings import sample_settings

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Enrich minimal graph JSON/YAML into ELK JSON.")
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Path to minimal input JSON/YAML",
    )
    parser.add_argument(
        "-s",
        "--settings",
        help="Path to settings TOML/JSON (optional)",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Where to write ELK JSON (default: stdout)",
    )
    args = parser.parse_args(argv)

    input_path = Path(args.input)
    if not input_path.exists():
        parser.error(f"input file not found: {input_path}")

    minimal = _load_input(args.input)

    settings = sample_settings()
    if args.settings:
        settings_path = Path(args.settings)
        if not settings_path.exists():
            parser.error(f"settings file not found: {settings_path}")
        settings = _load_settings(args.settings)

    canvas = build_canvas(minimal, settings)
    payload = canvas.model_dump(by_alias=True, exclude_none=True)
    output = json.dumps(payload, indent=2)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output)

    return 0

if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
