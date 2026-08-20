/* Shipped audit harness — version sync check. Version: v1.3
   Fails if ui_build/VERSION, version.js, any shipped file-header marker,
   the PROVENANCE current-version line, the rendered badge, or the tab title drift.

   Usage: node ui_build/audit/version_sync_test.js
*/
"use strict";
const fs = require("fs");
const path = require("path");
const assert = require("assert");
const REPO = path.resolve(path.join(__dirname, "..", ".."));

const VERSION = fs.readFileSync(path.join(REPO, "ui_build/VERSION"), "utf8").trim();
assert.ok(/^v\d+\.\d+$/.test(VERSION), `VERSION format: ${VERSION}`);

global.window = {};
require(path.join(REPO, "ui_build/app/version.js"));
assert.strictEqual(window.APP_VERSION, VERSION, "version.js matches VERSION file");

const files = [
  "ui_build/app/index.html", "ui_build/app/app.css", "ui_build/app/app.js",
  "ui_build/app/version.js", "ui_build/serve.py", "ui_build/build_index.py",
];
for (const f of files) {
  const txt = fs.readFileSync(path.join(REPO, f), "utf8");
  assert.ok(txt.includes(`Version: ${VERSION}`), `${f} header marker missing/stale`);
}
const prov = fs.readFileSync(path.join(REPO, "ui_build/PROVENANCE.md"), "utf8");
assert.ok(prov.includes(`**Current version: ${VERSION}**`), "PROVENANCE current-version line stale");

class El {
  constructor(tag) { this.tag = tag; this.children = []; this._v = ""; this._t = ""; this.innerHTML = ""; this.hidden = false; }
  get value() { return this._v; } set value(v) { this._v = v; }
  get textContent() { return this._t; } set textContent(v) { this._t = v; this.children = []; }
  appendChild(c) { this.children.push(c); return c; }
  addEventListener() {}
}
const byId = {};
global.document = {
  getElementById: id => (byId[id] ??= new El("div")),
  createElement: t => new El(t),
  createDocumentFragment: () => new El("#frag"),
  title: "",
};
const INDEX = JSON.parse(fs.readFileSync(path.join(REPO, "ui_build/app/index.json"), "utf8"));
global.fetch = async () => ({ ok: true, json: async () => INDEX });
require(path.join(REPO, "ui_build/app/app.js"));
setTimeout(() => {
  assert.strictEqual(byId["version-badge"].textContent, VERSION, "header badge shows version");
  assert.strictEqual(global.document.title, `Tennis UI ${VERSION}`, "tab title shows version");
  console.log(`VERSION SYNC PASS — ${VERSION} consistent across VERSION file, version.js, ${files.length} file headers, badge, and tab title`);
}, 20);
