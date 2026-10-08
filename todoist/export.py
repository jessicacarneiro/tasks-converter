from __future__ import annotations

import csv
from pathlib import Path

TASK_INDENT = 1
SUBTASK_INDENT = 2
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

Row = dict[str, str | int]


def task_row(content: str, indent: int) -> Row:
    return {
        "TYPE": "task",
        "CONTENT": content.strip(),
        "PRIORITY": DEFAULT_PRIORITY,
        "INDENT": indent,
        "AUTHOR": AUTHOR,
        "TIMEZONE": TIMEZONE,
        "DURATION_UNIT": DURATION_UNIT_NONE,
    }


def write_csv(rows: list[Row], csv_path: Path) -> None:
    with csv_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES, restval="")
        writer.writeheader()
        writer.writerows(rows)
    print(f"CSV written to {csv_path}")
    if len(rows) > TODOIST_MAX_TASKS:
        print(
            f"Warning: {len(rows)} tasks exceeds Todoist's limit of "
            f"{TODOIST_MAX_TASKS} per project; split the CSV before importing."
        )
