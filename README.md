# PPT Icon Studio

PPT Icon Studio is a Codex plugin marketplace containing the `ppt-icon-studio` plugin. The plugin helps Codex create custom icon assets that behave well in Microsoft PowerPoint.

It is built for natural-language requests such as:

- create a set of slide icons from a theme or keyword,
- convert a reference image into a scalable PowerPoint icon,
- convert an attached image into a PowerPoint-style icon,
- produce a flat editable SVG icon that can be recolored in slides,
- produce a high-resolution transparent PNG for 3D or textured icons.

## Install As A Codex Plugin

Add this GitHub repository as a Codex plugin marketplace:

```powershell
codex plugin marketplace add https://github.com/munkm1109-lang/ppt-icon-studio
```

Install the plugin from that marketplace:

```powershell
codex plugin add ppt-icon-studio@ppt-icon-studio
```

After the repository is updated, refresh and reinstall:

```powershell
codex plugin marketplace upgrade ppt-icon-studio
codex plugin add ppt-icon-studio@ppt-icon-studio
```

Start a new Codex thread after installation so the skill is loaded into the session.

## Usage

Use normal prompts. You should not need to paste the `SKILL.md` path.

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

## Repository Layout

```text
.agents/plugins/marketplace.json
plugins/ppt-icon-studio/.codex-plugin/plugin.json
plugins/ppt-icon-studio/skills/ppt-icon-studio/SKILL.md
plugins/ppt-icon-studio/skills/ppt-icon-studio/references/
plugins/ppt-icon-studio/skills/ppt-icon-studio/scripts/
```

## Optional Skill-Only Install

If you only want the skill files without installing the full Codex plugin, you can use the Skills CLI:

```powershell
npx skills add https://github.com/munkm1109-lang/ppt-icon-studio --skill ppt-icon-studio --full-depth
```

That is not the same as installing the Codex plugin. For normal Codex plugin use, prefer the `codex plugin marketplace add` flow above.

## Output Modes

The primary skill chooses one of four strategies:

1. **Editable PPT SVG** for simple monochrome, flat, monoline, geometric, business, or symbolic icons.
2. **Color Vector SVG** for flat multicolor icons where palette preservation matters.
3. **Reference Reconstruction SVG** for recreating a provided reference image as scalable SVG artwork.
4. **Complex Transparent Raster** for 3D, textured, photorealistic, or highly detailed icons.

## Notes

This is a skill-first plugin. It does not expose MCP callable tools such as `create_icon` or `normalize_svg`. The skill handles strategy selection and uses local helper scripts when the workflow needs image cleanup, tracing preparation, or color SVG conversion.
