# Task Tracker CLI

A command-line interface to track and manage tasks, built in Python. Tasks are stored persistently in a local JSON file — no database or external libraries required.

This project has been made as per https://roadmap.sh/projects/task-tracker instructions.

---

## Prerequisites

- Python 3.x

---

## Setup

```bash
git clone https://github.com/0902shreyanshg/Task-Tracker.git
cd Task-Tracker
```

---

## Usage

```bash
python3 task_cli.py <command> [arguments]
```

### Commands

| Command | Arguments | Description |
|---|---|---|
| `add` | `"description"` | Add a new task |
| `update` | `<id> "description"` | Update a task's description |
| `delete` | `<id>` | Delete a task |
| `mark-in-progress` | `<id>` | Mark a task as in-progress |
| `mark-done` | `<id>` | Mark a task as done |
| `list` | _(none)_ | List all tasks |
| `list` | `todo` / `in-progress` / `done` | List tasks filtered by status |

### Examples

```bash
# Add tasks
python3 task_cli.py add "Buy groceries"
python3 task_cli.py add "Cook dinner"

# Update a task
python3 task_cli.py update 1 "Buy groceries and cook dinner"

# Mark status
python3 task_cli.py mark-in-progress 1
python3 task_cli.py mark-done 2

# List tasks
python3 task_cli.py list
python3 task_cli.py list done
python3 task_cli.py list in-progress
python3 task_cli.py list todo

# Delete a task
python3 task_cli.py delete 1
```

---

## Task Properties

Each task stored in `tasks.json` has the following fields:

| Field | Type | Description |
|---|---|---|
| `id` | Integer | Unique identifier, auto-incremented from max existing ID |
| `description` | String | Task description |
| `status` | String | `todo`, `in-progress`, or `done` |
| `createdAt` | String | Timestamp when task was created |
| `updatedAt` | String | Timestamp when task was last modified |

---

## Architecture

The entire codebase is built on two concepts: **CLI** and **File System**.

### CLI — Reading User Input

Python receives command-line input as a list via `sys.argv`:

```
python3 task_cli.py add "Buy groceries"
['task_cli.py', 'add', 'Buy groceries']
  sys.argv[0]  sys.argv[1]  sys.argv[2]
```

- `sys.argv[0]` — filename (always present, never read explicitly)
- `sys.argv[1]` — command (`add`, `delete`, `update`, etc.)
- `sys.argv[2]` — description or task ID depending on command
- `sys.argv[3]` — new description (only for `update`)

### File System — Persistence via JSON

Tasks are stored in `tasks.json` in the current directory, created automatically on first use.

**Why JSON over alternatives:**
- Database (MySQL, PostgreSQL) — overkill for a local CLI tool
- Plain text file — no structure, hard to read back
- JSON file — structured, simple, no setup required

JSON is a universal format for structured data, readable by every programming language and by humans directly.

---

## Common Pattern Across Commands

Every command follows the same core sequence:

```
1. Validate inputs (edge cases)
2. Load tasks.json into memory
3. Perform the action on the in-memory list
4. Write the updated list back to tasks.json
5. Print confirmation
```

This is the fundamental backend pattern: **read → modify in memory → write back**. At scale, a database replaces the JSON file, but the pattern is identical.

---

## Variations Per Command

These are the notable deviations from the common pattern worth understanding:

**`list` does not write back.**
It only reads and prints. No modification occurs, so there is nothing to write back to the file.

**`list` accepts an optional filter argument.**
Unlike other commands where the third argument is required (or absent), `list` treats `sys.argv[2]` as optional. If present, tasks are filtered by status using list comprehension. If absent, all tasks are printed.

**`delete` uses list comprehension instead of a loop.**
Rather than finding and removing a specific item, it rebuilds the entire list excluding the deleted task:
```python
tasks = [task for task in tasks if task["id"] != task_id]
```

**`mark-in-progress` and `mark-done` store a different status value than the command name.**
The command is `mark-in-progress` but the stored status is `"in-progress"`. The command is `mark-done` but the stored status is `"done"`. The `mark-` prefix is just the CLI verb; the stored value is the clean status string.

**ID generation is collision-safe after deletions.**
```python
"id": max(task["id"] for task in tasks) + 1 if tasks else 1
```
Using `len(tasks) + 1` would cause ID collisions after deletions. Using the max existing ID guarantees uniqueness regardless of what has been deleted.

---

## Why Python

This project was built in Python because the `"no external libraries"` constraint makes JSON handling in other languages painful (Java has no JSON in the standard JDK; Rust requires `serde_json` which is external). Python's stdlib covers everything this project needs — `json`, `os`, `sys`, `datetime` — with minimal boilerplate, keeping the focus on backend concepts rather than language mechanics.

---

## Language-Agnostic Takeaway

This project could be built in any language. The concepts — CLI argument parsing, JSON serialisation, file I/O, CRUD operations, edge case handling — are universal backend fundamentals. The specific syntax changes; the mental model does not.
