#!/usr/bin/env python

import sys

for line in sys.stdin:
    if line.startswith("// "):
        sys.stdout.write(line[3:])
    else:
        sys.stdout.write("// " + line)
