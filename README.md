# PPT Icon Studio

PPT Icon Studio is a local Codex plugin for creating custom icon assets that behave well in Microsoft PowerPoint.

It is built for natural-language requests such as:

- create a set of slide icons from a theme or keyword,
- convert a reference image into a scalable PowerPoint icon,
- convert an attached image into a PowerPoint-style icon from natural language,
- produce a flat editable SVG icon that can be recolored in slides,
- produce a high-resolution transparent PNG for 3D or textured icons.

## Install

Install from this repository with the Skills CLI:

```powershell
npx skills add https://github.com/munkm1109-lang/ppt-icon-studio --skill ppt-icon-studio
```

For local Codex plugin development, this repository follows the standard plugin layout:

```text
.codex-plugin/plugin.json
skills/ppt-icon-studio/SKILL.md
skills/ppt-icon-studio/references/
skills/ppt-icon-studio/scripts/
```

## How To Use

After installing the plugin, use normal prompts. You should not need to paste the `SKILL.md` path.

Examples:

```text
이 이미지를 PPT 기본 아이콘처럼 단색 SVG로 만들어줘.
```

```text
첨부한 이미지를 파워포인트에서 쓸 투명 배경 아이콘으로 바꿔줘.
```

```text
Create five PPT-safe SVG icons for a cybersecurity risk management deck.
```

Korean trigger examples:

- `이 이미지를 PPT 기본 아이콘처럼 만들어줘`
- `파워포인트에서 쓸 단색 SVG 아이콘으로 바꿔줘`
- `레퍼런스 이미지 기반으로 투명 배경 아이콘 만들어줘`

## Output Modes

The primary skill chooses one of four strategies:

1. **Editable PPT SVG** for simple monochrome, flat, monoline, geometric, business, or symbolic icons.
2. **Color Vector SVG** for flat multicolor icons where palette preservation matters.
3. **Reference Reconstruction SVG** for recreating a provided reference image as scalable SVG artwork.
4. **Complex Transparent Raster** for 3D, textured, photorealistic, or highly detailed icons.

## PPT-Native Icon Profile

The default profile is `ppt-native-icon`:

- square canvas,
- `viewBox="0 0 512 512"`,
- transparent background,
- 10-16% visual padding,
- simple SVG paths when possible,
- no text nodes, embedded raster images, external assets, or fragile filters in editable SVG output,
- transparent PNG/WebP at 1024px or 2048px for complex raster output.

## Dependencies

The guidance works without every optional tool, but output quality improves when these are available:

- Python 3 with Pillow for crop, trace preparation, and alpha checks,
- `potrace` for monochrome SVG tracing,
- Node.js with `@neplex/vectorizer` and `sharp` for color SVG vectorization,
- ImageMagick for measurement and visual diffs,
- `rsvg-convert` or Sharp for SVG preview rendering,
- `svgo` for SVG optimization.

The skill reports which checks passed and which were skipped.

## Files

Final assets should be written to the user's requested destination or to:

```text
tmp/ppt-icon-studio/<request-slug>/
```

Intermediate files are intentionally preserved for review and iteration.

## Notes

This is a skill-first plugin. It does not expose MCP callable tools such as `create_icon` or `normalize_svg`. The skill handles strategy selection and uses local helper scripts when the workflow needs image cleanup, tracing preparation, or color SVG conversion.
