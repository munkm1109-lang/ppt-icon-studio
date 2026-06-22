#!/usr/bin/env python3
"""Prepare icon source images for PowerPoint-safe tracing.

This helper crops the visible subject, optionally removes a green chroma-key
background, writes a trimmed PNG, and for monochrome icons writes a PBM file
that can be passed to potrace.

Adapted from JKc66/custom-icons-skill for PPT Icon Studio.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from color_utils import parse_hex_color
from crop_trace_ops import process_icon


def main() -> None:
    parser = argparse.ArgumentParser(description="Crop and prepare a PPT icon source image.")
    parser.add_argument("source", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("name")
    parser.add_argument("--threshold", type=int, default=180)
    parser.add_argument("--chroma", action="store_true", help="Remove default green chroma key.")
    parser.add_argument("--key-color", type=parse_hex_color, default=(0, 255, 0))
    parser.add_argument("--tolerance", type=int, default=60)
    parser.add_argument("--padding", type=int, default=12)
    args = parser.parse_args()

    key = args.key_color if args.chroma else None
    process_icon(
        args.source,
        args.output_dir,
        args.name,
        threshold=args.threshold,
        chroma_key=key,
        tolerance=args.tolerance,
        padding=args.padding,
    )


if __name__ == "__main__":
    main()
