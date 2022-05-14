#!/usr/bin/env python3

import sys

def main():
    if len(sys.argv) < 2:
        print("USAGE: {} ARG".format(sys.argv[0]))
        sys.exit(1)

    arg = sys.argv[1]
    print(arg)

if __name__ == "__main__":
    main()
