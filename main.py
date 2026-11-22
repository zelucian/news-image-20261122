#!/usr/bin/env python3
"""Standard-library-only entry point for news-image-20261122.

Copies the pre-rendered entry.png from beside this file to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png),
creating the output directory if needed. No network, no
third-party imports.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)


if __name__ == "__main__":
    main()
