#!/usr/bin/env python3
"""Remove a flat chroma-key background from an icon image.

Writes a PNG or WebP with an alpha channel. Designed for 3D or detailed icons
that should be inserted into PowerPoint as high-resolution transparent raster
assets.

Adapted from JKc66/custom-icons-skill for PPT Icon Studio.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from chroma_alpha import apply_chroma_alpha, apply_edge_adjustments, validate_alpha_paths
from chroma_sampling import sample_border_key
from color_utils import parse_key_color
from pillow_utils import load_pillow


def remove_chroma_key(args: argparse.Namespace) -> None:
    image_mod, image_filter = load_pillow(filters=True)
    source = Path(args.input)
    output = Path(args.out)
    validate_alpha_paths(source, output, args.force)

    image = image_mod.open(source).convert("RGBA")
    key = sample_border_key(image, args.auto_key) if args.auto_key != "none" else args.key_color
    width, height = image.size
    transparent, partial = apply_chroma_alpha(image, key, args)
    image = apply_edge_adjustments(image, image_filter, args.edge_contract, args.edge_feather)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)
    total = width * height
    print(f"Wrote: {output}")
    print(f"Key color: #{key[0]:02x}{key[1]:02x}{key[2]:02x}")
    print(f"Transparent pixels before feathering: {transparent}/{total}")
    print(f"Partial pixels before feathering: {partial}/{total}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Remove chroma-key background from a PPT icon source.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--key-color", type=parse_key_color, default=(0, 255, 0))
    parser.add_argument("--auto-key", choices=["none", "corners", "border"], default="none")
    parser.add_argument("--tolerance", type=int, default=12)
    parser.add_argument("--soft-matte", action="store_true")
    parser.add_argument("--transparent-threshold", type=float, default=12.0)
    parser.add_argument("--opaque-threshold", type=float, default=96.0)
    parser.add_argument("--edge-feather", type=float, default=0.0)
    parser.add_argument("--edge-contract", type=int, default=0)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    remove_chroma_key(args)


if __name__ == "__main__":
    main()
