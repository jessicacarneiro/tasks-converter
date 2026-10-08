# tasks-converter

Converts a Hotmart course structure (modules and pages) into a CSV that can be imported into a Todoist project. Each module becomes a task and each of its pages becomes a sub-task.

## Requirements

- Python 3.14 (see `Pipfile`); no third-party dependencies

## Usage

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

2. From the project root, run the parser:

   ```bash
   python -m hotmart.parser path/to/modules.json
   ```

   This writes `path/to/modules.csv`. To choose a different output path:

   ```bash
   python -m hotmart.parser path/to/modules.json -o tasks.csv
   ```

3. In Todoist, open the target project and import the CSV (project menu → **Import from CSV**).

## Output format

The CSV follows [Todoist's CSV import template](https://todoist.com/help/articles/360000748525), UTF-8 encoded, with these columns:

| Column          | Value                                                          |
|-----------------|----------------------------------------------------------------|
| `TYPE`          | Always `task`                                                  |
| `CONTENT`       | The module or page name, with surrounding whitespace trimmed   |
| `DESCRIPTION`   | Empty                                                          |
| `PRIORITY`      | `4` (p4). Todoist treats an empty priority as p1, the highest  |
| `INDENT`        | `1` for a module (task), `2` for a page (sub-task)             |
| `AUTHOR`        | `Jéssica (28441054)`                                           |
| `TIMEZONE`      | `America/Sao_Paulo`                                            |
| `DURATION_UNIT` | `None` (no duration)                                           |
| `RESPONSIBLE`, `DATE`, `DATE_LANG`, `DURATION`, `DEADLINE`, `DEADLINE_LANG` | Empty, so Todoist uses its defaults |

Each module row is followed by its pages, in the order they appear in the JSON:

```csv
TYPE,CONTENT,DESCRIPTION,PRIORITY,INDENT,AUTHOR,RESPONSIBLE,DATE,DATE_LANG,TIMEZONE,DURATION,DURATION_UNIT,DEADLINE,DEADLINE_LANG
task,Comece aqui!,,4,1,Jéssica (28441054),,,,America/Sao_Paulo,,None,,
task,Comece aqui!,,4,2,Jéssica (28441054),,,,America/Sao_Paulo,,None,,
task,"O que é, de fato, um commonplace book?",,4,2,Jéssica (28441054),,,,America/Sao_Paulo,,None,,
task,Da curiosidade a pesquisa,,4,1,Jéssica (28441054),,,,America/Sao_Paulo,,None,,
task,"Como pesquisar, de verdade, sobre qualquer tema",,4,2,Jéssica (28441054),,,,America/Sao_Paulo,,None,,
```

### Todoist limits

- A project can hold at most 300 tasks per import. The parser prints a warning when the CSV has more rows than that; split the file and import it in batches.
- Any `@word` in a module or page name becomes a Todoist label.
- Rows with invalid values are silently skipped by Todoist, and an import can't be undone automatically.

`AUTHOR` and `TIMEZONE` are set as constants at the top of `hotmart/parser.py`; change them there to use a different account or time zone.

## Project structure

```
hotmart/
├── models.py   # Module and Page dataclasses built from the Hotmart JSON
└── parser.py   # CLI that converts the JSON into the Todoist CSV
```
