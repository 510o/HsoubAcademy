# Taskaty
A simple CLI task manager with dates and due-time tracking.

## Features
- Add tasks with title, description, start/end dates, and completion status.
- List tasks in a readable table with a dynamic "Due In" column (Today, Tomorrow, Xd overdue).
- Mark tasks as done, remove a specific task, remove all, or remove only completed tasks.
- Validates date ranges and task numbers.
- Supports both Unicode (default) and plain ASCII (`--ascii`) table borders.
- Stores tasks safely in JSON.

## Installation
```bash
git clone https://github.com/510o/HsoubAcademy.git
cd "HsoubAcademy/Python Application Development/Taskaty"
pip install -e .
```

## Usage
```bash
# Add a new task with a deadline
taskaty add "Clean my room" -e 2026-11-01

# Add a task and mark it as completed immediately
taskaty add "Read chapter 1" -D

# List pending tasks (Unicode table)
taskaty list

# List all tasks (including completed) using ASCII table for limited terminals
taskaty list -a --ascii

# Mark task 2 as completed
taskaty check 2

# Remove task 3
taskaty remove 3

# Remove all completed tasks
taskaty remove -D
```

## Example Output
```text
$ taskaty list
┌───┬────────────────┬─────────────┬────────────┬────────────┬────────┐
│ # │     Title      │ Description │ Start Date │  End Date  │ Due In │
├───┼────────────────┼─────────────┼────────────┼────────────┼────────┤
│ 1 │ Clean my room  │      —      │ 2026-10-22 │ 2026-11-01 │ in 10d │
│ 3 │ Read chapter 1 │      —      │ 2026-10-22 │     —      │  Open  │
└───┴────────────────┴─────────────┴────────────┴────────────┴────────┘
```

## Data Location
Tasks are stored in a secure user directory: ~/.taskaty/tasks.json.

## License
MIT