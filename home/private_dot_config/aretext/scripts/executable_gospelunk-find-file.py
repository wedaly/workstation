#!/usr/bin/env python3
import os
import sys
import subprocess

# Hack to change working directory to the directory containing the file,
# which should hopefully be inside a Go module.
# Need to translate the paths back so they show up correctly in aretext.
def main():
    if len(sys.argv) < 3:
        print("Usage: {} WORD PATH".format(sys.argv[0]))
        sys.exit(1)

    word, path = sys.argv[1], sys.argv[2]
    if os.path.isfile(path):
        path = os.path.dirname(path)

    cwd = path
    find_pkg_path = os.path.relpath(path, cwd)
    cmd = [
        "gospelunk", "find",
        "-i",
        "-f", "{{.Path}}:{{.LineNum}}:{{.Kind}} {{.Name}}",
        "^(.+\.)?{}$".format(word),
        find_pkg_path,
    ]
    output = subprocess.run(cmd, cwd=cwd, capture_output=True)
    for line in output.stdout.decode('utf-8').split("\n"):
        if line:
            matchpath, rest = line.split(":", 1)
            matchpath = os.path.relpath(matchpath)
            print("{}:{}".format(matchpath, rest))


if __name__ == "__main__":
    main()
