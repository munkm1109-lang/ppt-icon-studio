# Reference Image Workflow

Use this when a user supplies a reference image and wants a scalable SVG recreation or a cleaned slide icon based on it.

## Setup

Create a work directory:

```text
tmp/ppt-icon-studio/<request-slug>/
  original.png
  refs/
  parts/
  final.svg
  icon-preview.png
```

Keep the original image unchanged.

## Analysis

Measure before drawing:

1. Identify original image dimensions.
2. Determine the subject bounding box.
3. Map the subject to a 512x512 SVG canvas.
4. Record the largest visual parts as layers.
5. Decide which parts are expression-critical or identity-critical.

For PPT icons, prefer fewer, clearer layers over exhaustive pixel-level reconstruction.

## Decomposition

Split by visual function:

- background or container shape,
- primary symbol,
- secondary marks,
- highlights or shadows,
- outline or border.

For paired elements, build them consistently. For repeated elements, reuse geometry when practical.

## Reconstruction

Build each part as standalone SVG in `parts/` when the image is complex. Use simple primitives for geometric shapes and paths for custom silhouettes.

All part SVGs should share the final canvas:

```xml
viewBox="0 0 512 512"
```

## Comparison

When ImageMagick and an SVG renderer are available:

1. Render the current SVG to PNG.
2. Resize the reference to the same canvas.
3. Compare proportions and silhouette first.
4. Fix the largest three visible mismatches.
5. Check small-size readability at 64px and 128px.

Do not chase pixel-perfect reproduction when it hurts icon clarity. For slides, a clear and reusable icon is better than a noisy exact trace.
