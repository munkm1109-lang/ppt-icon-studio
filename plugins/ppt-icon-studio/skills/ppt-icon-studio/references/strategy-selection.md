# Strategy Selection

Pick exactly one primary strategy before creating files. If a request mixes strategies, choose the one that best preserves PowerPoint usability and note the tradeoff.

## Strategy A: Editable PPT SVG

Use for:

- monoline icons,
- flat business icons,
- simple symbols,
- geometric icons,
- icons the user wants to recolor inside PowerPoint.

Preferred pipeline:

```text
concept/theme/reference
  -> simple high-contrast source
  -> crop_and_trace.py
  -> potrace SVG when available
  -> SVG cleanup and PPT-safe normalization
  -> preview render
```

Output should be a single-color or stroke-based SVG. Avoid multi-color fills unless the user explicitly requests them.

## Strategy B: Color Vector SVG

Use for:

- flat multicolor icons,
- palette-preserving icon illustrations,
- simple AI-generated raster sources that should become scalable SVG.

Preferred pipeline:

```text
raster source
  -> remove connected background
  -> convert_color_svg.js
  -> PPT-safe SVG review
  -> preview render
```

This strategy preserves colors, but PowerPoint recoloring will be less native than Strategy A.

## Strategy C: Reference Reconstruction SVG

Use for:

- the user provides a reference image,
- the desired result should be a cleaner scalable recreation,
- the subject has multiple meaningful parts that should be rebuilt deliberately.

Preferred pipeline:

```text
reference image
  -> measure canvas and subject bounds
  -> identify feature layers
  -> create reference crops
  -> rebuild SVG layers
  -> render and compare
  -> final composite SVG
```

Use this for quality over speed. Do not use it for one-off simple icons that Strategy A can handle.

## Strategy D: Complex Transparent Raster

Use for:

- 3D rendered icons,
- textured icons,
- photorealistic or glossy icons,
- detailed objects that would vectorize poorly.

Preferred pipeline:

```text
source on flat chroma-key background
  -> remove_chroma_key.py
  -> trim and center
  -> export transparent PNG/WebP at 1024px and 2048px
  -> preview and alpha checks
```

Do not claim this output is PowerPoint-editable. It is PowerPoint-ready but raster-based.

## Defaults

If the user says "like PowerPoint icons" or "editable", choose Strategy A.

If the user says "same colors", "illustration", or "flat colorful", choose Strategy B.

If the user gives a reference image and wants a faithful vector version, choose Strategy C.

If the user says "3D", "realistic", "glossy", "texture", or "high resolution PNG", choose Strategy D.
