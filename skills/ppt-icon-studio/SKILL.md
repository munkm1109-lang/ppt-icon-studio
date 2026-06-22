---
name: ppt-icon-studio
description: Use when the user asks in natural language to make PowerPoint/PPT icons, convert an attached image or reference image into an icon, create PPT-safe SVG/PNG assets, make editable single-color SVG icons, or says Korean prompts like "이미지를 아이콘으로", "파워포인트 아이콘", "PPT 기본 아이콘처럼", "투명 SVG/PNG 아이콘", or "레퍼런스 이미지로 아이콘 만들어줘".
---

# PPT Icon Studio

Use this skill automatically when the user wants custom icons for PowerPoint from a theme, keyword, concept, style direction, attached image, or reference image. This includes natural Korean requests such as:

- "이미지를 아이콘으로 만들어줘"
- "파워포인트에서 쓸 아이콘으로 바꿔줘"
- "PPT 기본 아이콘처럼 단색 SVG로 만들어줘"
- "레퍼런스 이미지 기반으로 아이콘 만들어줘"
- "투명 배경 PNG/SVG 아이콘으로 만들어줘"

The goal is not generic image generation. The goal is slide-ready icon assets that behave like PowerPoint icons whenever possible: scalable, transparent, aligned on a square canvas, visually simple at small sizes, and easy to recolor when the chosen style allows it.

## Required Reading

Before creating assets, read only the references needed for the chosen route:

- `references/strategy-selection.md` for every request.
- `references/ppt-safe-svg.md` for every SVG request.
- `references/reference-image-workflow.md` when the user provides a reference image or asks for an SVG recreation.
- `references/verification.md` before final delivery.

## Workflow

1. Identify the user inputs:
   - subject, theme, or keyword,
   - target style,
   - attached images or reference image paths,
   - desired output type,
   - target destination, if provided.
2. Choose one strategy:
   - Editable PPT SVG,
   - Color Vector SVG,
   - Reference Reconstruction SVG,
   - Complex Transparent Raster.
3. Create a visible work directory:

```text
tmp/ppt-icon-studio/<request-slug>/
```

Keep source images, intermediate crops, traced files, SVG drafts, previews, and final files there unless the user specifies another final destination. Do not delete intermediates unless the user asks.

4. Build the asset using the selected strategy.
5. Normalize final output to the `ppt-native-icon` profile where applicable.
6. Verify the final assets using `references/verification.md`.
7. Report:
   - selected strategy,
   - final file paths,
   - intermediate workspace,
   - checks passed,
   - checks skipped because tools were unavailable.

## Output Defaults

For SVG routes, produce:

```text
icon.svg
icon-ppt-safe.svg
icon-preview.png
```

For complex raster routes, produce:

```text
icon-1024.png
icon-2048.png
icon-preview.png
```

## Scripts

Scripts are stored in `scripts/`:

- `crop_and_trace.py`: crop, binarize, and prepare PBM files for monochrome tracing.
- `remove_chroma_key.py`: remove a flat chroma-key background and preserve alpha.
- `convert_color_svg.js`: convert a raster image to a color SVG with transparent background cleanup.

Prefer these scripts over retyping large code blocks when they fit the request.

## Design Rules

- SVG is preferred for PowerPoint icons that need scaling or recoloring.
- Transparent high-resolution PNG/WebP is preferred for 3D, detailed, textured, or photorealistic icons.
- Do not force detailed raster artwork into editable SVG if the result would be noisy or hard to edit.
- For editable SVG, favor simple paths, solid fills, normalized strokes, and no text nodes.
- For icons that must work at small slide sizes, validate at 64px and 128px when possible.

## Missing Details

Ask one concise question only when a missing detail blocks strategy selection or output destination. If the request already includes a subject and an intended style, proceed with sensible defaults:

- output profile: `ppt-native-icon`,
- canvas: 512x512 SVG or 2048px raster master,
- padding: 12%,
- background: transparent,
- final location: `tmp/ppt-icon-studio/<request-slug>/`.
