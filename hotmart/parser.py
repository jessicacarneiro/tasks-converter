from __future__ import annotations

import argparse
import json
from pathlib import Path

from hotmart.models import Module
from todoist.export import SUBTASK_INDENT, TASK_INDENT, Row, task_row, write_csv


def load_modules(json_path: Path) -> list[Module]:
    with json_path.open(encoding="utf-8") as file:
        data = json.load(file)
    return [Module.from_dict(module) for module in data.get("modules", [])]


def to_rows(modules: list[Module]) -> list[Row]:
    rows: list[Row] = []
    for module in modules:
        rows.append(task_row(module.name, TASK_INDENT))
        for page in module.pages:
            rows.append(task_row(page.name, SUBTASK_INDENT))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a Hotmart modules JSON into a Todoist-importable CSV."
    )
    parser.add_argument("json_path", type=Path, help="Path to the Hotmart JSON file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Path to the output CSV (defaults to the JSON path with a .csv extension)",
    )
    args = parser.parse_args()

    csv_path = args.output or args.json_path.with_suffix(".csv")
    write_csv(to_rows(load_modules(args.json_path)), csv_path)


if __name__ == "__main__":
    main()
