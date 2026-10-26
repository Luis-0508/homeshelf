// Builds dist/preview/index.html: app/index.html with the Tizen mock loaded
// first, so the real app code runs in a desktop browser at 1920x1080.
// Usage: node scripts/preview/build.mjs
import { copyFileSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";

const out = "dist/preview";
mkdirSync(out, { recursive: true });
const html = readFileSync("app/index.html", "utf8");
if (!html.includes("</head>")) {
  console.error("app/index.html: no </head> to inject the mock before");
  process.exit(1);
}
writeFileSync(`${out}/index.html`, html.replace("</head>", '<script src="tizen-mock.js"></script>\n</head>'));
copyFileSync("scripts/preview/tizen-mock.js", `${out}/tizen-mock.js`);
console.log(`${out}/index.html built`);
