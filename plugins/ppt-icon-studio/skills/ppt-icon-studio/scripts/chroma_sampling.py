"""Background key sampling helpers."""

from __future__ import annotations

from statistics import median
import sys


def sample_border_key(image, mode: str) -> tuple[int, int, int]:
    width, height = image.size
    pixels = image.load()
    samples = corner_samples(pixels, width, height) if mode == "corners" else border_samples(pixels, width, height)

    if not samples:
        print("Error: could not sample key color from image border.", file=sys.stderr)
        raise SystemExit(1)

    return (
        int(round(median(pixel[0] for pixel in samples))),
        int(round(median(pixel[1] for pixel in samples))),
        int(round(median(pixel[2] for pixel in samples))),
    )


def corner_samples(pixels, width: int, height: int) -> list[tuple[int, int, int]]:
    patch = max(1, min(width, height, 12))
    boxes = [
        (0, 0, patch, patch),
        (width - patch, 0, width, patch),
        (0, height - patch, patch, height),
        (width - patch, height - patch, width, height),
    ]
    samples: list[tuple[int, int, int]] = []
    for left, top, right, bottom in boxes:
        for y in range(top, bottom):
            samples.extend(pixels[x, y][:3] for x in range(left, right))
    return samples


def border_samples(pixels, width: int, height: int) -> list[tuple[int, int, int]]:
    band = max(1, min(width, height, 6))
    step = max(1, min(width, height) // 256)
    samples: list[tuple[int, int, int]] = []
    for x in range(0, width, step):
        samples.extend(pixels[x, y][:3] for y in range(band))
        samples.extend(pixels[x, height - 1 - y][:3] for y in range(band))
    for y in range(0, height, step):
        samples.extend(pixels[x, y][:3] for x in range(band))
        samples.extend(pixels[width - 1 - x, y][:3] for x in range(band))
    return samples
