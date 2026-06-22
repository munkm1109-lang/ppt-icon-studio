"""Crop and trace-preparation operations."""

from __future__ import annotations

from pathlib import Path
import sys

from color_utils import channel_distance
from pillow_utils import load_pillow


def remove_chroma(image, key: tuple[int, int, int], tolerance: int):
    data = []
    for red, green, blue, alpha in image.getdata():
        transparent = channel_distance((red, green, blue), key) <= tolerance
        data.append((0, 0, 0, 0) if transparent else (red, green, blue, alpha))
    image.putdata(data)
    return image


def visible_bbox(image, chroma: bool):
    _image, image_ops = load_pillow()
    if chroma:
        return image.getchannel("A").getbbox()
    gray = image_ops.grayscale(image.convert("RGB"))
    mask = gray.point(lambda pixel: 255 if pixel < 245 else 0)
    return mask.getbbox()


def crop_with_padding(image, bbox, padding: int):
    if not bbox:
        return image
    left, top, right, bottom = bbox
    return image.crop(
        (
            max(0, left - padding),
            max(0, top - padding),
            min(image.width, right + padding),
            min(image.height, bottom + padding),
        )
    )


def write_monochrome_pbm(image, image_ops, output_dir: Path, name: str, threshold: int) -> None:
    gray = image_ops.grayscale(image.convert("RGB"))
    bw = gray.point(lambda pixel: 0 if pixel < threshold else 255, mode="1")
    pbm_path = output_dir / f"{name}.pbm"
    bw.save(pbm_path)
    print(f"PBM: {pbm_path}")
    print("Trace with: potrace <file>.pbm --svg --flat -o <file>.svg")


def process_icon(
    source: Path,
    output_dir: Path,
    name: str,
    *,
    threshold: int,
    chroma_key: tuple[int, int, int] | None,
    tolerance: int,
    padding: int,
) -> None:
    image_mod, image_ops = load_pillow()
    if not source.exists():
        print(f"Error: source image not found: {source}", file=sys.stderr)
        raise SystemExit(1)

    output_dir.mkdir(parents=True, exist_ok=True)
    image = image_mod.open(source).convert("RGBA")

    if chroma_key is not None:
        image = remove_chroma(image, chroma_key, tolerance)

    image = crop_with_padding(image, visible_bbox(image, chroma_key is not None), padding)
    png_path = output_dir / f"{name}.png"
    image.save(png_path)
    print(f"PNG: {png_path}")

    if chroma_key is None:
        write_monochrome_pbm(image, image_ops, output_dir, name, threshold)
