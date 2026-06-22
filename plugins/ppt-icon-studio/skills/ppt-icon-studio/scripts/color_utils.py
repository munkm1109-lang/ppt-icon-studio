"""Small color helpers for PPT Icon Studio scripts."""

from __future__ import annotations

import argparse
import re


def parse_hex_color(value: str, *, label: str = "color") -> tuple[int, int, int]:
    raw = value.strip().lstrip("#")
    if len(raw) != 6:
        raise argparse.ArgumentTypeError(f"{label} must be a hex RGB value like #00ff00")
    try:
        return int(raw[0:2], 16), int(raw[2:4], 16), int(raw[4:6], 16)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"{label} must be a hex RGB value like #00ff00") from exc


def parse_key_color(raw: str) -> tuple[int, int, int]:
    match = re.fullmatch(r"#?([0-9a-fA-F]{6})", raw.strip())
    if not match:
        raise argparse.ArgumentTypeError("key color must look like #00ff00")
    return parse_hex_color(match.group(1), label="key color")


def channel_distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2]))
