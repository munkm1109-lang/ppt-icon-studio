# PPT-Safe SVG Profile

Use this profile for SVG assets intended for Microsoft PowerPoint.

## `ppt-native-icon`

```text
viewBox: 0 0 512 512
canvas: square
padding: 10-16%
default padding: 12%
background: transparent
preferred geometry: paths, circles, rects, ellipses, and simple groups
editable color mode: single fill or single stroke color
fallback color mode: flat multicolor fills
```

## SVG Rules

The root SVG must include:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
```

For editable icon output:

- use solid `fill` or `stroke`,
- keep stroke widths consistent,
- use `stroke-linecap="round"` and `stroke-linejoin="round"` for monoline icons,
- avoid fractional visual imbalance by centering the subject inside the canvas,
- keep shapes visually legible at 64px.

## Avoid For PPT Editable Icons

Avoid these unless the strategy explicitly requires color illustration:

- `<text>` elements,
- `<image>` elements,
- external links or remote assets,
- CSS classes that PowerPoint may ignore,
- complex masks,
- heavy filters,
- clip paths that can be replaced by simple paths,
- excessive gradients,
- thousands of tiny vectorized paths.

## Normalization Checklist

- The icon fits in a square canvas.
- The visual subject has 10-16% padding.
- The background is transparent.
- The SVG has a `viewBox`.
- No external files are referenced.
- The file opens as standalone SVG.
- A PNG preview was rendered or a skipped-render reason was reported.

## When To Use PNG Instead

Use a transparent PNG/WebP fallback when the icon depends on:

- 3D lighting,
- realistic texture,
- soft shadows,
- photographic detail,
- dense color transitions,
- many tiny shapes after vectorization.

In these cases, create a 2048px master and optionally a 1024px delivery copy.
