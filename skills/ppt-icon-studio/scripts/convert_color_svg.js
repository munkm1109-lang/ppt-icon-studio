#!/usr/bin/env node
/*
 * Convert a raster icon source into a color SVG with transparent background.
 *
 * Adapted from heroygt/skills svg-icon-maker for PPT Icon Studio.
 *
 * Dependencies:
 *   npm install @neplex/vectorizer sharp
 *
 * Usage:
 *   node convert_color_svg.js <input-image> [output-dir]
 */

const fs = require("fs");
const path = require("path");
const sharp = require("sharp");
const { vectorize, ColorMode, Hierarchical, PathSimplifyMode } = require("@neplex/vectorizer");

const inputFile = process.argv[2];
const outputRoot = process.argv[3] || path.join("tmp", "ppt-icon-studio", "color-svg");

if (!inputFile) {
  console.error("Usage: node convert_color_svg.js <input-image> [output-dir]");
  process.exit(1);
}

if (!fs.existsSync(inputFile)) {
  console.error(`Input file not found: ${inputFile}`);
  process.exit(1);
}

const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
const jobDir = path.join(outputRoot, timestamp);
fs.mkdirSync(jobDir, { recursive: true });

const copiedReference = path.join(jobDir, "reference.png");
const preprocessedPng = path.join(jobDir, "reference-transparent.png");
const outputSvg = path.join(jobDir, "icon.svg");
const outputPreview = path.join(jobDir, "icon-preview.png");

function stripSvgBackground(svg) {
  return svg
    .replace(/<rect\b[^>]*(?:width="100%"|width="\d+")[^>]*(?:height="100%"|height="\d+")[^>]*\bfill="[^"]+"[^>]*\/?>/gi, "")
    .replace(/style="[^"]*background[^"]*"/gi, (match) => {
      const styleValue = match.slice(7, -1);
      const cleaned = styleValue
        .split(";")
        .map((part) => part.trim())
        .filter((part) => part && !/^background\s*:/i.test(part))
        .join(";");
      return cleaned ? `style="${cleaned}"` : "";
    });
}

async function preprocessToTransparentPng(inputPath, outputPath, threshold = 30) {
  const image = sharp(inputPath).ensureAlpha();
  const { data, info } = await image.raw().toBuffer({ resolveWithObject: true });
  const { width, height } = info;
  const bgR = data[0];
  const bgG = data[1];
  const bgB = data[2];
  const visited = new Uint8Array(width * height);
  const queue = [];

  function enqueueIfBackground(x, y) {
    const index = (y * width + x) * 4;
    const diff = Math.abs(data[index] - bgR) + Math.abs(data[index + 1] - bgG) + Math.abs(data[index + 2] - bgB);
    const visitedIndex = y * width + x;
    if (diff <= threshold * 3 && visited[visitedIndex] === 0) {
      visited[visitedIndex] = 1;
      queue.push([x, y]);
    }
  }

  enqueueIfBackground(0, 0);
  enqueueIfBackground(width - 1, 0);
  enqueueIfBackground(0, height - 1);
  enqueueIfBackground(width - 1, height - 1);

  let removed = 0;
  while (queue.length > 0) {
    const [x, y] = queue.pop();
    const index = (y * width + x) * 4;
    data[index + 3] = 0;
    removed += 1;

    for (const [nextX, nextY] of [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]) {
      if (nextX < 0 || nextY < 0 || nextX >= width || nextY >= height) {
        continue;
      }
      const visitedIndex = nextY * width + nextX;
      if (visited[visitedIndex] !== 0) {
        continue;
      }
      const pixelIndex = visitedIndex * 4;
      if (data[pixelIndex + 3] === 0) {
        continue;
      }
      const diff = Math.abs(data[pixelIndex] - bgR) + Math.abs(data[pixelIndex + 1] - bgG) + Math.abs(data[pixelIndex + 2] - bgB);
      if (diff <= threshold * 3) {
        visited[visitedIndex] = 1;
        queue.push([nextX, nextY]);
      }
    }
  }

  const transparentBuffer = await sharp(data, {
    raw: { width, height, channels: 4 },
  }).png().toBuffer();

  await fs.promises.writeFile(outputPath, transparentBuffer);
  console.log(`Background pixels removed: ${removed}/${width * height}`);
  return transparentBuffer;
}

async function main() {
  fs.copyFileSync(inputFile, copiedReference);
  console.log(`Job directory: ${jobDir}`);

  const inputBuffer = await preprocessToTransparentPng(inputFile, preprocessedPng);
  let svg = await vectorize(inputBuffer, {
    colorMode: ColorMode.Color,
    hierarchical: Hierarchical.Stacked,
    filterSpeckle: 8,
    colorPrecision: 6,
    layerDifference: 32,
    mode: PathSimplifyMode.Spline,
    cornerThreshold: 60,
    lengthThreshold: 4.0,
    maxIterations: 10,
    spliceThreshold: 45,
  });

  svg = stripSvgBackground(svg);
  await fs.promises.writeFile(outputSvg, svg, "utf8");
  await sharp(Buffer.from(svg)).resize(512, 512, { fit: "contain" }).png().toFile(outputPreview);

  console.log(`SVG: ${outputSvg}`);
  console.log(`Preview: ${outputPreview}`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
