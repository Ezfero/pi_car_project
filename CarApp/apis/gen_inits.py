#!/usr/bin/env python3
import os
import sys

if len(sys.argv) < 2:
    print("Usage: create_init.py <gen-directory>")
    sys.exit(1)

gen_dir = sys.argv[1]
py_dir = os.path.join(gen_dir, "py")

for path in [gen_dir, py_dir]:
    init_file = os.path.join(path, "__init__.py")
    if not os.path.exists(init_file):
        open(init_file, "a").close()
        print(f"Created {init_file}")