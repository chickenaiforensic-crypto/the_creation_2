/* Shipped audit harness — Task 1 tournament/player filter verification. Version: v1.5
   Loads the real app.js with a DOM stub, drives the filters, and cross-checks
   every count against the RAW engine edition files (independent code path).

   Usage: node ui_build/audit/ui_filter_test.js
*/
"use strict";
const fs = require("fs");
const path = require("path");
const assert = require("assert");

const REPO = path.resolve(path.join(__dirname, "..", ".."));
const ENGINE = path.join(REPO, "ui_build/engine");

/* ---------- independent ground truth from raw engine bytes ---------- */
const manifest = JSON.parse(fs.readFileSync(path.join(ENGINE, "MANIFEST.json"), "utf8"));
const rawMatches = [];
for (const e of manifest.editions) {
  const d = JSON.parse(fs.readFileSync(path.join(ENGINE, e.file_path), "utf8"));
  assert.strictEqual(d.matches.length, e.match_count, `raw count ${e.file_path}`);
  for (const r of d.matches) rawMatches.push(r);
}
const truth = { total: rawMatches.length, byKey: {}, playersByKey: {}, allPlayers: new Set() };
for (const r of rawMatches) {
  const key = `${r.tournament}|${r.tour}`;
  (truth.byKey[key] ??= []).push(r);
  (truth.playersByKey[key] ??= new Set()).add(r.playerA).add(r.playerB);
  truth.allPlayers.add(r.playerA).add(r.playerB);
}

/* ---------- minimal DOM stub ---------- */
class El {
  constructor(tag) {
    this.tag = tag; this.children = []; this._listeners = {};
    this._value = ""; this._text = ""; this.innerHTML = ""; this.hidden = false;
  }
  get value() { return this._value; }
  set value(v) { this._value = v; }
  get textContent() { return this._text; }
  set textContent(v) { this._text = v; this.children = []; }
  appendChild(c) { this.children.push(c); return c; }
  addEventListener(ev, fn) { (this._listeners[ev] ??= []).push(fn); }
  dispatch(ev) { for (const fn of this._listeners[ev] ?? []) fn(); }
  rows() { return this.children.flatMap(c => (c.tag === "#frag" ? c.children : [c])); }
  optionValues() { return this.children.map(c => c.value); }
}
const byId = {};
global.document = {
  getElementById: id => (byId[id] ??= new El("div")),
  createElement: t => new El(t),
  createDocumentFragment: () => new El("#frag"),
};
const INDEX = JSON.parse(fs.readFileSync(path.join(REPO, "ui_build/app/index.json"), "utf8"));
global.fetch = async () => ({ ok: true, json: async () => INDEX });

require(path.join(REPO, "ui_build/app/app.js"));
const tick = () => new Promise(r => setImmediate(r));

(async () => {
  await tick(); await tick();

  const tSel = byId["tournament-select"], pSel = byId["player-select"];
  const pFilter = byId["player-filter-input"], body = byId["matches-body"];
  const count = byId["result-count"], strip = byId["data-strip"], empty = byId["empty-state"];

  /* stub-only: index.html ships a static <option value="">All tournaments</option>
     that the stub did not parse — seed it so fillTournaments appended after it. */
  const allOpt = new El("option"); allOpt.value = ""; allOpt.textContent = "All tournaments";
  tSel.children.unshift(allOpt);

  /* 1. initial state = full dataset (year filter defaults to all years) */
  assert.strictEqual(strip.textContent,
    `78 editions · ${truth.total.toLocaleString("en-US")} matches · ${Object.keys(truth.byKey).length} tournaments · ${truth.allPlayers.size} players`,
    "data strip");
  assert.strictEqual(tSel.children.length, 1 + Object.keys(truth.byKey).length, "tournament options");
  assert.strictEqual(pSel.children.length, 1 + truth.allPlayers.size, "player options (all)");
  assert.strictEqual(count.textContent, `${truth.total.toLocaleString("en-US")} matches`, "count all");
  assert.strictEqual(body.rows().length, 401, "render cap 400 + note row");

  /* 2. every tournament: player list + match count vs raw bytes */
  for (const key of Object.keys(truth.byKey)) {
    tSel.value = key; tSel.dispatch("change");
    const expectedPlayers = [...truth.playersByKey[key]].sort((a, b) => a.toLowerCase() < b.toLowerCase() ? -1 : 1);
    assert.deepStrictEqual(pSel.optionValues().slice(1), expectedPlayers, `player list ${key}`);
    const n = truth.byKey[key].length;
    assert.strictEqual(count.textContent, `${n.toLocaleString("en-US")} match${n === 1 ? "" : "es"}`, `count ${key}`);
    assert.strictEqual(body.rows().length, Math.min(n, 400) + (n > 400 ? 1 : 0), `rows ${key}`);
    assert.strictEqual(empty.hidden, true, `empty hidden ${key}`);
  }

  /* 3. tournament + player: cross-check vs raw bytes for several keys */
  const samples = ["Tokyo|ATP", "US Open|WTA", "Cincinnati|WTA", "Basel|ATP", "Zhengzhou|WTA"];
  for (const key of samples) {
    tSel.value = key; tSel.dispatch("change");
    for (const p of [...truth.playersByKey[key]].slice(0, 3)) {
      pSel.value = p; pSel.dispatch("change");
      const n = truth.byKey[key].filter(r => r.playerA === p || r.playerB === p).length;
      assert.strictEqual(count.textContent, `${n.toLocaleString("en-US")} match${n === 1 ? "" : "es"}`, `count ${key}/${p}`);
      assert.strictEqual(body.rows().length, Math.min(n, 400) + (n > 400 ? 1 : 0), `rows ${key}/${p}`);
    }
  }

  /* 4. player selected with no tournament = global player filter */
  tSel.value = ""; tSel.dispatch("change");
  const anyPlayer = [...truth.allPlayers][0];
  pSel.value = anyPlayer; pSel.dispatch("change");
  const nGlob = rawMatches.filter(r => r.playerA === anyPlayer || r.playerB === anyPlayer).length;
  assert.strictEqual(count.textContent, `${nGlob.toLocaleString("en-US")} match${nGlob === 1 ? "" : "es"}`, "global player count");

  /* 5. text filter narrows player options but never loses the selection */
  tSel.value = "US Open|ATP"; tSel.dispatch("change");
  const target = [...truth.playersByKey["US Open|ATP"]].find(p => p.length > 8);
  pSel.value = target; pSel.dispatch("change");
  pFilter.value = target.slice(0, 4); pFilter.dispatch("input");
  assert.ok(pSel.optionValues().includes(target), "selection retained under text filter");
  const narrowed = pSel.optionValues().slice(1).filter(v => v);
  for (const v of narrowed) {
    assert.ok(v.toLowerCase().includes(target.slice(0, 4).toLowerCase()) || v === target, `narrowed ${v}`);
  }

  /* 6. switching to a tournament without the selected player resets the player */
  pFilter.value = ""; pFilter.dispatch("input");
  const outsider = [...truth.playersByKey["Zhengzhou|WTA"]][0];
  tSel.value = "Zhengzhou|WTA"; tSel.dispatch("change");
  pSel.value = outsider; pSel.dispatch("change");
  tSel.value = "Basel|ATP"; tSel.dispatch("change");
  assert.strictEqual(pSel.value, "", "player reset when absent from new tournament");
  assert.strictEqual(count.textContent,
    `${truth.byKey["Basel|ATP"].length.toLocaleString("en-US")} matches`, "count after reset");

  /* 7. reset returns to full dataset */
  byId["reset-btn"].dispatch("click");
  assert.strictEqual(tSel.value, "", "reset tournament");
  assert.strictEqual(pSel.value, "", "reset player");
  assert.strictEqual(count.textContent, `${truth.total.toLocaleString("en-US")} matches`, "reset count");
  assert.strictEqual(pSel.children.length, 1 + truth.allPlayers.size, "reset player options");

  console.log("ALL UI FILTER TESTS PASSED");
  console.log(`ground truth: ${truth.total} matches, ${Object.keys(truth.byKey).length} tournaments, ${truth.allPlayers.size} players`);
})().catch(e => { console.error("TEST FAILURE:", e.message); process.exit(1); });
