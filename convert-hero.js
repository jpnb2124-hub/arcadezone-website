// Step 3 helper: convert the hero SVG into optimized WebP and AVIF files.
// Run this after installing sharp: npm install sharp --no-audit --no-fund
// Then run: node convert-hero.js
const sharp = require("sharp");
const fs = require("fs");
(async () => {
  const svg = fs.readFileSync("./images/hero.svg");
  await sharp(svg).resize(1200,420, {fit: 'cover'}).webp({quality:80}).toFile("./images/hero.webp");
  await sharp(svg).resize(1200,420, {fit: 'cover'}).avif({quality:50}).toFile("./images/hero.avif");
  console.log("Converted hero.svg -> hero.webp + hero.avif");
})();
