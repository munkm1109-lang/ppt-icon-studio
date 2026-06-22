# Verification

Run the checks that match the output type. Report passed and skipped checks in the final response.

## SVG Checks

Required when possible:

```powershell
xmllint --noout icon-ppt-safe.svg
```

If `xmllint` is unavailable, inspect the SVG for a valid root element and balanced tags.

Check the root includes:

```text
xmlns="http://www.w3.org/2000/svg"
viewBox="0 0 512 512"
```

Search for risky constructs:

```powershell
Select-String -Path icon-ppt-safe.svg -Pattern '<text|<image|filter=|<filter|<mask|<foreignObject|http://|https://'
```

Risky constructs are not always forbidden, but they must be reported.

## Preview Render

Render a preview when a renderer is available:

```powershell
rsvg-convert -w 512 -h 512 icon-ppt-safe.svg -o icon-preview.png
```

Alternative renderers such as Sharp, ImageMagick, or a browser screenshot are acceptable.

## Small-Size Check

When possible, render:

```powershell
rsvg-convert -w 64 -h 64 icon-ppt-safe.svg -o icon-64.png
rsvg-convert -w 128 -h 128 icon-ppt-safe.svg -o icon-128.png
```

The icon should still read clearly at both sizes.

## Raster Alpha Check

For PNG/WebP output, confirm transparent corners. With Python and Pillow:

```powershell
python -c "from PIL import Image; im=Image.open('icon-2048.png').convert('RGBA'); w,h=im.size; print([im.getpixel(p)[3] for p in [(0,0),(w-1,0),(0,h-1),(w-1,h-1)]])"
```

Expected: all corner alpha values are `0` or near `0`.

## Dimension Check

For raster output:

```powershell
python -c "from PIL import Image; im=Image.open('icon-2048.png'); print(im.size)"
```

Expected: square output, usually `(2048, 2048)` or `(1024, 1024)`.

## Final Report

Always report:

- selected strategy,
- final paths,
- work directory,
- passed checks,
- skipped checks with tool names,
- whether the output is editable SVG or raster slide asset.
