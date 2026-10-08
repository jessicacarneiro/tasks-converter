from __future__ import annotations

import argparse
import json
from pathlib import Path

from todoist.export import SUBTASK_INDENT, TASK_INDENT, Row, task_row, write_csv
from udemy.models import Chapter, CurriculumItem, CurriculumPage, Lecture


def load_items(json_paths: list[Path]) -> list[CurriculumItem]:
    items: list[CurriculumItem] = []
    for json_path in json_paths:
        with json_path.open(encoding="utf-8") as file:
            items.extend(CurriculumPage.from_dict(json.load(file)).results)
    return items


def to_rows(items: list[CurriculumItem]) -> list[Row]:
    rows: list[Row] = []
    for item in items:
        if isinstance(item, Chapter):
            rows.append(task_row(item.title, TASK_INDENT))
        elif isinstance(item, Lecture):
            # A lecture before any chapter has no parent, so keep it top-level
            indent = SUBTASK_INDENT if rows else TASK_INDENT
            rows.append(task_row(item.title, indent))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert Udemy curriculum JSON pages into a Todoist-importable CSV."
    )
    parser.add_argument(
        "json_paths",
        type=Path,
        nargs="+",
        help="Paths to the Udemy curriculum JSON files, in page order",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Path to the output CSV (defaults to the first JSON path with a .csv extension)",
    )
    args = parser.parse_args()

    csv_path = args.output or args.json_paths[0].with_suffix(".csv")
    write_csv(to_rows(load_items(args.json_paths)), csv_path)


if __name__ == "__main__":
    main()
