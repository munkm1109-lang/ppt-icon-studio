"""Chroma-key alpha processing helpers."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from color_utils import channel_distance


def alpha_for_distance(distance: int, transparent_at: float, opaque_at: float) -> int:
    if distance <= transparent_at:
        return 0
    if distance >= opaque_at:
        return 255
    ratio = (distance - transparent_at) / (opaque_at - transparent_at)
    smooth = ratio * ratio * (3 - 2 * ratio)
    return max(0, min(255, int(round(255 * smooth))))


def validate_alpha_paths(source: Path, output: Path, force: bool) -> None:
    if not source.exists():
        print(f"Error: input image not found: {source}", file=sys.stderr)
        raise SystemExit(1)
    if output.suffix.lower() not in {".png", ".webp"}:
        print("Error: output must be .png or .webp to preserve alpha.", file=sys.stderr)
        raise SystemExit(1)
    if output.exists() and not force:
        print(f"Error: output exists: {output}. Use --force to overwrite.", file=sys.stderr)
        raise SystemExit(1)


def pixel_alpha(distance: int, alpha: int, args: argparse.Namespace) -> int:
    new_alpha = (
        alpha_for_distance(distance, args.transparent_threshold, args.opaque_threshold)
        if args.soft_matte
        else (0 if distance <= args.tolerance else 255)
    )
    return int(round(new_alpha * (alpha / 255.0)))


def apply_chroma_alpha(image, key: tuple[int, int, int], args: argparse.Namespace) -> tuple[int, int]:
    pixels = image.load()
    width, height = image.size
    transparent = 0
    partial = 0
    for y in range(height):
        row_transparent, row_partial = apply_chroma_row(pixels, y, width, key, args)
        transparent += row_transparent
        partial += row_partial
    return transparent, partial


def apply_chroma_row(
    pixels,
    y: int,
    width: int,
    key: tuple[int, int, int],
    args: argparse.Namespace,
) -> tuple[int, int]:
    transparent = 0
    partial = 0
    for x in range(width):
        red, green, blue, alpha = pixels[x, y]
        new_alpha = pixel_alpha(channel_distance((red, green, blue), key), alpha, args)
        if new_alpha == 0:
            transparent += 1
            pixels[x, y] = (0, 0, 0, 0)
            continue
        partial += 1 if new_alpha < 255 else 0
        pixels[x, y] = (red, green, blue, new_alpha)
    return transparent, partial


def apply_edge_adjustments(image, image_filter, edge_contract: int, edge_feather: float):
    if edge_contract:
        alpha = image.getchannel("A")
        for _ in range(edge_contract):
            alpha = alpha.filter(image_filter.MinFilter(3))
        image.putalpha(alpha)

    if edge_feather:
        alpha = image.getchannel("A").filter(image_filter.GaussianBlur(radius=edge_feather))
        image.putalpha(alpha)
    return image
