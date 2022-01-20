#!/usr/bin/env python3
import os
import sys
import subprocess


# Hack to change working directory to the directory containing the file,
# which should hopefully be inside a Go module.
def main():
    if len(sys.argv) < 2:
        print("Usage: {} PATH".format(sys.argv[0]))
        sys.exit(1)

    path = sys.argv[1]
    if os.path.isfile(path):
        path = os.path.dirname(path)

    cwd = path
    index_pkg_path = os.path.relpath(path, cwd)
    print("Indexing {} from directory {}".format(path, cwd))
    subprocess.run(["gospelunk", "index", "-i", "-t", index_pkg_path], cwd=cwd)


if __name__ == "__main__":
    main()
