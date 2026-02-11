"""Example entrypoint: enrich minimal graph JSON into ELK JSON.

Run:
    python main.py -i json/sample_input_01.json -s json/elk_settings.example.toml -o /tmp/elk.json
"""

import argparse
import json
from pathlib import Path

from elkpydantic.builder import MinimalGraphIn, build_canvas, _load_settings
from elkpydantic.settings import sample_settings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Enrich minimal graph JSON into ELK JSON.")
    parser.add_argument(
        "-i",
        "--input",
        default="json/sample_input_01.json",
        help="Path to minimal input JSON (default: json/sample_input_01.json)",
    )
    parser.add_argument(
        "-s",
        "--settings",
        default="json/elk_settings.example.toml",
        help="Path to settings TOML/JSON (default: json/elk_settings.example.toml)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="json/output_test.json",
        help="Where to write ELK JSON (default: stdout)",
    )
    args = parser.parse_args(argv)

    with Path(args.input).open("r", encoding="utf-8") as f:
        minimal = MinimalGraphIn.model_validate_json(f.read())

    settings = None
    if args.settings and Path(args.settings).exists():
        settings = _load_settings(args.settings)
    else:
        settings = sample_settings()

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
