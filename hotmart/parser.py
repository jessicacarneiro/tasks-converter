from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from hotmart.models import Module

MODULE_INDENT = 1
PAGE_INDENT = 2
# An empty PRIORITY makes Todoist default to p1 (highest), so set p4 explicitly
DEFAULT_PRIORITY = 4
DURATION_UNIT_NONE = "None"
AUTHOR = "Jéssica (28441054)"
TIMEZONE = "America/Sao_Paulo"
TODOIST_MAX_TASKS = 300

# Column order from Todoist's CSV template:
# https://todoist.com/help/articles/360000748525
FIELDNAMES = [
    "TYPE",
    "CONTENT",
    "DESCRIPTION",
    "PRIORITY",
    "INDENT",
    "AUTHOR",
    "RESPONSIBLE",
    "DATE",
    "DATE_LANG",
    "TIMEZONE",
    "DURATION",
    "DURATION_UNIT",
    "DEADLINE",
    "DEADLINE_LANG",
]


def load_modules(json_path: Path) -> list[Module]:
    with json_path.open(encoding="utf-8") as file:
        data = json.load(file)
    return [Module.from_dict(module) for module in data.get("modules", [])]


def task_row(content: str, indent: int) -> dict[str, str | int]:
    return {
        "TYPE": "task",
        "CONTENT": content.strip(),
        "PRIORITY": DEFAULT_PRIORITY,
        "INDENT": indent,
        "AUTHOR": AUTHOR,
        "TIMEZONE": TIMEZONE,
        "DURATION_UNIT": DURATION_UNIT_NONE,
    }


def to_rows(modules: list[Module]) -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    for module in modules:
        rows.append(task_row(module.name, MODULE_INDENT))
        for page in module.pages:
            rows.append(task_row(page.name, PAGE_INDENT))
    return rows


def write_csv(rows: list[dict[str, str | int]], csv_path: Path) -> None:
    with csv_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES, restval="")
        writer.writeheader()
        writer.writerows(rows)


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
    rows = to_rows(load_modules(args.json_path))
    write_csv(rows, csv_path)
    print(f"CSV written to {csv_path}")
    if len(rows) > TODOIST_MAX_TASKS:
        print(
            f"Warning: {len(rows)} tasks exceeds Todoist's limit of "
            f"{TODOIST_MAX_TASKS} per project; split the CSV before importing."
        )


if __name__ == "__main__":
    main()
