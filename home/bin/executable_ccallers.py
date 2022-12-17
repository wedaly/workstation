#!/usr/bin/env python3

import subprocess
import sys
import os


def main():
    if len(sys.argv) < 2:
        print("USAGE: {} SYMBOL".format(sys.argv[0]))
        sys.exit(1)

    target_symbol = sys.argv[1]

    dir = find_dir_with_cscope_file(os.getcwd())
    if dir is None:
        print("Could not find cscope file")
        sys.exit(1)

    for line in search_cscope(dir, target_symbol):
        file_loc = cscope_line_to_file_loc(dir, line)
        if file_loc is not None:
            print(file_loc)


def find_dir_with_cscope_file(d):
    while len(d) > 0 and d != "/":
        if os.path.exists(os.path.join(d, "cscope.files")):
            return d
        d = os.path.dirname(d)
    return None


def search_cscope(dir, symbol):
    result = subprocess.run(
        ["cscope", "-L3{}".format(symbol)],
        cwd=dir,
        check=True,
        capture_output=True)
    return [line for line in result.stdout.decode('utf-8').split("\n") if len(line) > 0]


def cscope_line_to_file_loc(dir, line):
    path, _, line_num, snippet = line.split(" ", 3)
    path = os.path.join(dir, path)
    return "{}:{}:{}".format(path, line_num, snippet)


if __name__ == "__main__":
    main()

