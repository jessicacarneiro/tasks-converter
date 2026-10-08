# tasks-converter

Converts online course structures into a CSV that can be imported into a Todoist project, so each course section becomes a task and each lesson becomes a sub-task. Supported sources:

- **Hotmart**: each module becomes a task and each of its pages becomes a sub-task.
- **Udemy**: each chapter becomes a task and each of its lectures becomes a sub-task.

## Requirements

- Python 3.14 (see `Pipfile`); no third-party dependencies

## Usage

Run the parsers from the project root. Then, in Todoist, open the target project and import the CSV (project menu → **Import from CSV**).

### Hotmart

1. Save the Hotmart modules JSON to a file. It must have a top-level `modules` list, where each module has a `name` and a list of `pages`:

   ```json
   {
       "modules": [
           {
               "name": "Comece aqui!",
               "pages": [
                   { "name": "Comece aqui!" },
                   { "name": "O que é, de fato, um commonplace book?" }
               ]
           }
       ]
   }
   ```

   The real response contains more fields (`id`, `hash`, `locked`, etc.); see `hotmart/models.py` for the full shape.

2. Run the parser:

   ```bash
   python -m hotmart.parser path/to/modules.json
   ```

   This writes `path/to/modules.csv`. To choose a different output path:

   ```bash
   python -m hotmart.parser path/to/modules.json -o tasks.csv
   ```

### Udemy

1. Get the course's curriculum JSON from your browser:

   1. Open the course on Udemy and open the browser's developer tools (**Network** tab).
   2. Reload the page and filter the requests by `subscriber-curriculum-items`.
   3. Open that request's response and save it to a file.

   The JSON has a flat `results` list, where each item has a `_class` and a `title`. Each `lecture` belongs to the `chapter` that comes before it:

   ```json
   {
       "count": 286,
       "next": "https://www.udemy.com/api-2.0/courses/.../?page=2&page_size=200",
       "previous": null,
       "results": [
           { "_class": "chapter", "title": "Getting Started" },
           { "_class": "lecture", "title": "Welcome to the Course" },
           { "_class": "quiz", "title": "Images & Containers" }
       ]
   }
   ```

   The real response contains more fields (`id`, `asset`, `sort_order`, etc.); see `udemy/models.py` for the full shape.

2. Run the parser:

   ```bash
   python -m udemy.parser path/to/curriculum.json
   ```

   The response is paginated: when `next` isn't `null`, there are more `subscriber-curriculum-items` requests (one per page, with `page=2`, `page=3`, etc. in the URL). Save each page to its own file and pass them all, in page order, so lectures at the start of a page stay under the chapter from the previous page:

   ```bash
   python -m udemy.parser page-1.json page-2.json -o tasks.csv
   ```

   The CSV defaults to the first JSON path with a `.csv` extension.

Only chapters and lectures are exported; quizzes and practice exercises are skipped. A lecture that appears before any chapter is exported as a top-level task.

## Output format

The CSV follows [Todoist's CSV import template](https://todoist.com/help/articles/360000748525), UTF-8 encoded, with these columns:

| Column          | Value                                                          |
|-----------------|----------------------------------------------------------------|
| `TYPE`          | Always `task`                                                  |
| `CONTENT`       | The Hotmart module or page `name`, or the Udemy chapter or lecture `title`, with surrounding whitespace trimmed |
| `DESCRIPTION`   | Empty                                                          |
| `PRIORITY`      | `4` (p4). Todoist treats an empty priority as p1, the highest  |
| `INDENT`        | `1` for a module or chapter (task), `2` for a page or lecture (sub-task) |
| `AUTHOR`        | `Jéssica (28441054)`                                           |
| `TIMEZONE`      | `America/Sao_Paulo`                                            |
| `DURATION_UNIT` | `None` (no duration)                                           |
| `RESPONSIBLE`, `DATE`, `DATE_LANG`, `DURATION`, `DEADLINE`, `DEADLINE_LANG` | Empty, so Todoist uses its defaults |

Each task row is followed by its sub-tasks, in the order they appear in the JSON:

```csv
TYPE,CONTENT,DESCRIPTION,PRIORITY,INDENT,AUTHOR,RESPONSIBLE,DATE,DATE_LANG,TIMEZONE,DURATION,DURATION_UNIT,DEADLINE,DEADLINE_LANG
task,Comece aqui!,,4,1,Jéssica (28441054),,,,America/Sao_Paulo,,None,,
task,Comece aqui!,,4,2,Jéssica (28441054),,,,America/Sao_Paulo,,None,,
task,"O que é, de fato, um commonplace book?",,4,2,Jéssica (28441054),,,,America/Sao_Paulo,,None,,
task,Da curiosidade a pesquisa,,4,1,Jéssica (28441054),,,,America/Sao_Paulo,,None,,
task,"Como pesquisar, de verdade, sobre qualquer tema",,4,2,Jéssica (28441054),,,,America/Sao_Paulo,,None,,
```

### Todoist limits

- A project can hold at most 300 tasks per import. The parsers print a warning when the CSV has more rows than that; split the file and import it in batches.
- Any `@word` in a task name becomes a Todoist label.
- Rows with invalid values are silently skipped by Todoist, and an import can't be undone automatically.

`AUTHOR` and `TIMEZONE` are set as constants at the top of `todoist/export.py`; change them there to use a different account or time zone.

## Project structure

```
hotmart/
├── models.py   # Module and Page dataclasses built from the Hotmart JSON
└── parser.py   # CLI that converts the Hotmart JSON into the Todoist CSV
udemy/
├── models.py   # Chapter, Lecture, Quiz, Practice and Asset dataclasses built from the Udemy JSON
└── parser.py   # CLI that converts the Udemy JSON pages into the Todoist CSV
todoist/
└── export.py   # Shared Todoist CSV columns, defaults and writer
```
