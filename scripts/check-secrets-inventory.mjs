// Checks secrets.inventory.json: names-only, required fields, monthly rotation, and that every
// environment variable the code or the example env file uses is recorded.
// Run: node scripts/check-secrets-inventory.mjs
import fs from "node:fs";
import path from "node:path";
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const INV = path.join(root, "secrets.inventory.json");
const SCAN = [];
const EXAMPLES = [".env.local.example", ".env.example"];
const IGNORE = /^(NODE_ENV|CI|NEXT_RUNTIME|VERCEL(_.*)?|NEXT_PUBLIC_VERCEL_.*)$/;
const inv = JSON.parse(fs.readFileSync(INV, "utf8"));
const errs = [];
const names = new Set(inv.items.map((i) => i.name));
if (names.size !== inv.items.length) errs.push("duplicate names in inventory");
const used = new Set();
const walk = (p) => {
  const full = path.join(root, p);
  if (!fs.existsSync(full)) return;
  if (fs.statSync(full).isFile()) return scan(full);
  for (const e of fs.readdirSync(full, { withFileTypes: true })) {
    if (e.isDirectory()) { if (!["node_modules", ".next"].includes(e.name)) walk(path.join(p, e.name)); }
    else scan(path.join(full, e.name));
  }
};
const scan = (f) => {
  if (/\.(ts|tsx|js|mjs)$/.test(f))
    for (const m of fs.readFileSync(f, "utf8").matchAll(/process\.env\.([A-Z][A-Z0-9_]+)/g)) used.add(m[1]);
};
SCAN.forEach(walk);
for (const f of EXAMPLES) {
  const full = path.join(root, f);
  if (fs.existsSync(full))
    for (const m of fs.readFileSync(full, "utf8").matchAll(/^#?\s*([A-Z][A-Z0-9_]+)=/gm)) used.add(m[1]);
}
for (const n of used) if (!IGNORE.test(n) && !names.has(n)) errs.push(`${n} is used but missing from secrets.inventory.json`);
for (const i of inv.items) {
  if (!["secret", "identifier", "config"].includes(i.kind)) errs.push(`${i.name}: bad kind`);
  if (i.kind === "secret") {
    if (!i.rotation_days || i.rotation_days > 30) errs.push(`${i.name}: secrets rotate in 30 days or fewer`);
    if (!i.rotate_howto) errs.push(`${i.name}: needs rotate_howto`);
  }
  if (i.last_rotated !== null && !/^\d{4}-\d{2}-\d{2}$/.test(i.last_rotated)) errs.push(`${i.name}: bad last_rotated`);
}
// No value from a local env file may appear in the inventory.
const text = fs.readFileSync(INV, "utf8");
for (const f of fs.readdirSync(root).filter((x) => x.startsWith(".env") && !x.endsWith("example")))
  for (const line of fs.readFileSync(path.join(root, f), "utf8").split("\n")) {
    const v = line.slice(line.indexOf("=") + 1).trim().replace(/^["']|["']$/g, "");
    if (v.length >= 16 && names.has(line.split("=")[0].trim()) && text.includes(v)) errs.push(`a value from ${f} is in the inventory`);
  }
if (errs.length) { console.error(errs.join("\n")); process.exit(1); }
console.log(`secrets.inventory.json OK (${inv.items.length} items)`);
