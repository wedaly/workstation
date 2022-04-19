#!/usr/bin/env python3

from contextlib import contextmanager
from datetime import date, datetime
import os
import subprocess
import sys
import textwrap

USAGE = """devlog <command>

COMMANDS:
    todo     Open tasks in an editor.
    edit     Open today's devlog entry in an editor.
    tail     Print last devlog entries to stdout.
    tidy     Move completed tasks to done file.
    sync     Commit and push the devlog git repository.
    migrate  Migrate from old devlog format.
"""

DEFAULT_DEVLOG_DIR = os.path.expanduser("~/devlogs")
DEFAULT_EDITOR = "nano"

DEVLOG_DIR = os.environ.get("DEVLOG_DIR", DEFAULT_DEVLOG_DIR)
EDITOR = os.environ.get("EDITOR", DEFAULT_EDITOR)
TODO_PATH = os.path.join(DEVLOG_DIR, "todo.txt")
DONE_PATH = os.path.join(DEVLOG_DIR, "done.txt")


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
    elif cmd == "migrate":
        run_migrate_cmd()
    else:
        print_usage_and_exit()


def print_usage_and_exit():
    print(USAGE)
    sys.exit(1)


def run_todo_cmd():
    open_editor(TODO_PATH)


def run_edit_cmd():
    today = date.today()
    month_dir = os.path.join(DEVLOG_DIR, str(today.year), "{:02}".format(today.month))
    os.makedirs(month_dir, exist_ok=True)
    day_path = os.path.join(month_dir, "{:02}.md".format(today.day))
    open_editor(day_path)


def run_tail_cmd():
    with chdir(DEVLOG_DIR):
        paths = []
        for root, dir, files in os.walk("."):
            for name in files:
                if name.endswith(".md"):
                    paths.append(os.path.join(root, name))

        # iterate descending by date
        paths.sort(reverse=True)
        for p in paths:
            date = datetime.strptime(p, "./%Y/%m/%d.md").strftime("%Y-%m-%d")
            sys.stdout.write("======= {} ========\n".format(date))
            with open(p) as f:
                for line in f:
                    sys.stdout.write(line)
            sys.stdout.write("\n")


def run_tidy_cmd():
    complete_tasks = []
    incomplete_tasks = []
    with open(TODO_PATH) as f:
        for line in f:
            if line.startswith("x "):
                complete_tasks.append(line)
            else:
                incomplete_tasks.append(line)

    complete_date = date.today().strftime("%Y-%m-%d")
    with open(DONE_PATH, "a") as f:
        for line in complete_tasks:
            line = line.strip() + " completed:{}\n".format(complete_date)
            f.write(line)

    with open(TODO_PATH, "w") as f:
        for line in incomplete_tasks:
            f.write(line)


def run_sync_cmd():
    with chdir(DEVLOG_DIR):
        git_cmd(["add", "."])
        git_cmd(["commit", "-m", "devlog sync"])
        git_cmd(["fetch", "origin"])
        git_cmd(["rebase", "origin/master"])
        git_cmd(["push", "origin"])


def run_migrate_cmd():
    with chdir(DEVLOG_DIR):
       for root, dir, files in os.walk("."):
            for name in files:
                if name.endswith(".devlog"):
                    path = os.path.join(root, name)
                    migrate_devlog(path)


def migrate_devlog(path):
    date = None
    entries = []
    line_num = 0
    with open(path) as f:
        for line in f:
            if line_num == 0:
                try:
                    date = datetime.strptime(line.strip(), "%Y-%m-%d")
                except:
                    print("Could not convert {}".format(path))
                    return
            else:
                if line.startswith("+ ") or line.startswith("- ") or line.startswith("* ") or line.startswith("^ "):
                    entries.append({"heading": line[2:].strip(), "lines": []})
                elif line.startswith("~~~"):
                    entries.append({"heading": "", "lines": []})
                elif len(entries) > 0:
                    entries[-1]["lines"].append(line.rstrip())

            line_num += 1

    real_entries = []
    for entry in entries:
        x = {
            "heading": entry["heading"],
            "content": textwrap.dedent("\n".join(entry["lines"])),
        }
        if len(x["content"].strip()) > 0:
            real_entries.append(x)

    if len(real_entries) == 0:
        return

    target_dir = os.path.join(str(date.year), "{:02}".format(date.month))
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, "{:02}.md".format(date.day))
    with open(target_path, "w") as f:
        for entry in real_entries:
            if len(entry["content"].replace("\n", "").strip()) > 0:
                if entry["heading"]:
                    f.write("# {}\n\n".format(entry["heading"]))
                f.write(entry["content"])
                f.write("\n")

    os.remove(path)


def git_cmd(args):
    print("git {}".format(" ".join(args)))
    subprocess.run(["git"] + args)


def open_editor(path):
    with chdir(DEVLOG_DIR):
        subprocess.run([EDITOR, path])


@contextmanager
def chdir(path):
    wd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(wd)


if __name__ == "__main__":
    main()
