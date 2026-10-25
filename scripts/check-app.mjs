// Syntax-checks the inline script of app/index.html without running it.
// Usage: node scripts/check-app.mjs [path/to/index.html]
import { readFileSync } from "node:fs";
import vm from "node:vm";

const file = process.argv[2] ?? "app/index.html";
const html = readFileSync(file, "utf8");
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map((m) => m[1]);

if (scripts.length === 0) {
  console.error(`${file}: no inline <script> found`);
  process.exit(1);
}

scripts.forEach((code, i) => {
  try {
    new vm.Script(code, { filename: `${file}#script${i + 1}` });
  } catch (error) {
    console.error(error.message);
    process.exit(1);
  }
});
console.log(`${file}: ${scripts.length} inline script(s) OK`);
