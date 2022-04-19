#!/usr/bin/env python3

from datetime import date
import os
import shutil
import subprocess
import sys

USAGE = """devlog <command>

COMMANDS:
    todo    Open tasks in an editor.
    edit    Open today's devlog entry in an editor.
    tail    Print last devlog entries to stdout.
    tidy    Remove completed tasks and sort tasks.
    sync    Commit and push the devlog git repository.
"""

DEFAULT_DEVLOG_DIR = "~/devlogs"
DEFAULT_EDITOR = "nano"

DEVLOG_DIR = os.environ.get("DEVLOG_DIR", DEFAULT_DEVLOG_DIR)
EDITOR = shutil.which(os.environ.get("EDITOR", DEFAULT_EDITOR))


def main():
    if len(sys.argv) < 2:
        print_usage_and_exit()

    cmd = sys.argv[1]
    if cmd == "todo":
        run_todo_cmd()
    elif cmd == "edit":
        run_edit_cmd()
    elif cmd == "tail":
        run_tail_cmd()
    elif cmd == "tidy":
        run_tidy_cmd()
    elif cmd == "sync":
        run_sync_cmd()
    else:
        print_usage_and_exit()


def print_usage_and_exit():
    print(USAGE)
    sys.exit(1)


def run_todo_cmd():
    path = os.path.join(DEVLOG_DIR, "todo.txt")
    subprocess.run([EDITOR, path])


def run_edit_cmd():
    today = date.today()
    month_dir = os.path.join(DEVLOG_DIR, str(today.year), "{:02}".format(today.month))
    os.makedirs(month_dir, exist_ok=True)
    day_path = os.path.join(month_dir, "{:02}.md".format(today.day))
    subprocess.run([EDITOR, day_path])


def run_tail_cmd():
    print("TODO")


def run_tidy_cmd():
    print("TODO")


def run_sync_cmd():
    print("TODO")


if __name__ == "__main__":
    main()
