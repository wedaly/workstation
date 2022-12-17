#!/usr/bin/env python3

import re
import subprocess
import sys
import os


def main():
    if len(sys.argv) < 2:
        print("USAGE: {} SYMBOL".format(sys.argv[0]))
        sys.exit(1)

    target_symbol = sys.argv[1]

    d = find_dir_with_tags_file(os.getcwd())
    if d is None:
        print("Could not find tags file")
        sys.exit(1)

    for tag in search_tags(d, target_symbol):
        f = tag_to_file_loc(d, tag)
        if f is not None:
            print(f)


def find_dir_with_tags_file(d):
    while len(d) > 0 and d != "/":
        if os.path.exists(os.path.join(d, "tags")):
            return d
        d = os.path.dirname(d)
    return None


def search_tags(dir, symbol):
    result = subprocess.run(
        ["readtags", "-i", "-", symbol],
        cwd=dir,
        check=True,
        capture_output=True)
    return [tag for tag in result.stdout.decode('utf-8').split("\n") if len(tag) > 0]


PATTERN_RE = re.compile(r"\/(.+)\/")

def tag_to_file_loc(dir, tag):
    # The tags(5) man page says that the pattern might also be a decimal line number
    # or a regex delimited by "?", but for now we just handle the /^ABC$/ regex form.
    symbol, path, pattern = tag.split('\t', maxsplit=2)
    match = PATTERN_RE.search(pattern)
    if match is None:
        return None

    path = os.path.join(dir, path)
    snippet = match.group(1)

    if snippet.startswith("^"):
        snippet = snippet[1:]
    if snippet.endswith("$"):
        snippet = snippet[:-1]

    line = lookup_line_num(path, snippet)
    if line is None:
        return None

    return "{}:{}:{}".format(path, line, snippet)


def lookup_line_num(path, snippet):
    with open(path) as f:
        for i, line in enumerate(f):
            if line.strip().startswith(snippet.strip()):
                return i + 1
    return None


if __name__ == "__main__":
    main()

