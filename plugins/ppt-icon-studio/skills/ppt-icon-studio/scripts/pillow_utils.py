"""Pillow loading helpers for PPT Icon Studio scripts."""

from __future__ import annotations

import sys


def load_pillow(*, filters: bool = False):
    try:
        from PIL import Image, ImageFilter, ImageOps
    except ImportError:
        print("Error: Pillow is required. Install with: pip install pillow", file=sys.stderr)
        raise SystemExit(1)
    return (Image, ImageFilter) if filters else (Image, ImageOps)
