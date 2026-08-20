/* Shipped audit harness — Phase 0 leaderboard verification. Version: v1.4
   Drives the REAL app.js leaderboard through tournament/year filters and compares
   every rendered cell against the independent Python ground truth.

   Usage: node ui_build/audit/lb_ui_test.js <lb_truth.json>
   (produce the truth file first: python3 ui_build/audit/lb_ground_truth.py /tmp/lb_truth.json)
*/
"use strict";
const fs = require("fs");
const path = require("path");
const assert = require("assert");

const REPO = path.resolve(path.join(__dirname, "..", ".."));
const TRUTH = JSON.parse(fs.readFileSync(process.argv[2] || "/tmp/lb_truth.json", "utf8"));
const INDEX = JSON.parse(fs.readFileSync(path.join(REPO, "ui_build/app/index.json"), "utf8"));

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
}
const byId = {};
global.document = {
  getElementById: id => (byId[id] ??= new El("div")),
  createElement: t => new El(t),
  createDocumentFragment: () => new El("#frag"),
};
global.fetch = async () => ({ ok: true, json: async () => INDEX });

require(path.join(REPO, "ui_build/app/app.js"));
const tick = () => new Promise(r => setImmediate(r));

function decode(s) {
  return s.replace(/<[^>]*>/g, "")
    .replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"').replace(/&#39;/g, "'");
}
function lbRows() {
  return byId["leaderboard-body"].rows().map(tr =>
    [...tr.innerHTML.matchAll(/<td[^>]*>(.*?)<\/td>/gs)].map(m => decode(m[1])));
}
function lbMetaNums() {
  const t = byId["leaderboard-meta"].textContent;
  const g = /([\d,]+) matches · ([\d,]+) players rated · ([\d,]+) sets scored · (\d+) incomplete sets excluded · (\d+) walkovers/.exec(t);
  assert.ok(g, `lb meta format: ${t}`);
  return { matches: +g[1].replace(/,/g, ""), players: +g[2].replace(/,/g, ""),
    setsCounted: +g[3].replace(/,/g, ""), setsExcluded: +g[4], walkovers: +g[5] };
}

(async () => {
  await tick(); await tick();
  const tSel = byId["tournament-select"], ySel = byId["year-select"];
  const mk = (v, txt) => { const o = new El("option"); o.value = v; o.textContent = txt; return o; };
  tSel.children.unshift(mk("", "All tournaments"));

  const scenarios = [
    ["ALL|", "", ""],
    ["ALL|2025", "", "2025"],
    ["Basel|ATP|2025", "Basel|ATP", "2025"],
    ["Basel|ATP|", "Basel|ATP", ""],
    ["US Open|WTA|2023", "US Open|WTA", "2023"],
    ["Cincinnati|WTA|", "Cincinnati|WTA", ""],
    ["Dubai|ATP|2024", "Dubai|ATP", "2024"],
    ["Zhengzhou|WTA|2023", "Zhengzhou|WTA", "2023"],
  ];

  for (const [key, tkey, year] of scenarios) {
    tSel.value = tkey; tSel.dispatch("change");
    ySel.value = year; ySel.dispatch("change");
    const exp = TRUTH[key];
    const got = lbRows();
    assert.strictEqual(got.length, exp.rows.length, `${key}: row count ${got.length} != ${exp.rows.length}`);
    for (let i = 0; i < exp.rows.length; i++) {
      const e = exp.rows[i].map(String), g = got[i];
      for (let c = 0; c < 6; c++) {
        const col = ["POS", "PLAYER", "RATING", "MATCHES", "AVG", "ACTUAL"][c];
        assert.strictEqual(g[c], e[c], `${key} row ${i} ${col}: ${g[c]} != ${e[c]} (${g[1]})`);
      }
    }
    assert.deepStrictEqual(lbMetaNums(), exp.meta, `${key}: meta mismatch`);
    const ratings = got.map(r => parseInt(r[2], 10));
    for (let i = 1; i < ratings.length; i++) assert.ok(ratings[i - 1] >= ratings[i], `${key} sort at ${i}`);
    assert.strictEqual(byId["leaderboard-warn"].hidden, true, `${key}: warn hidden`);
  }

  /* Task-1 regression under all three filters */
  tSel.value = "Basel|ATP"; tSel.dispatch("change");
  ySel.value = "2025"; ySel.dispatch("change");
  const pSel = byId["player-select"];
  const somePlayer = INDEX.playersByTournament["Basel|ATP"][0];
  pSel.value = somePlayer; pSel.dispatch("change");
  const n = INDEX.matches.filter(m => m.tkey === "Basel|ATP" && m.year === "2025" &&
    (m.playerA === somePlayer || m.playerB === somePlayer)).length;
  assert.strictEqual(byId["result-count"].textContent,
    `${n.toLocaleString("en-US")} match${n === 1 ? "" : "es"}`, "match log count under all three filters");

  /* reset restores full scope everywhere */
  byId["reset-btn"].dispatch("click");
  assert.strictEqual(lbRows().length, TRUTH["ALL|"].rows.length, "reset leaderboard rows");
  assert.strictEqual(ySel.value, "", "reset year");
  assert.strictEqual(byId["result-count"].textContent,
    `${INDEX.matches.length.toLocaleString("en-US")} matches`, "reset match log");

  console.log("ALL PHASE 0 LEADERBOARD TESTS PASSED");
  console.log(`scopes verified: ${scenarios.length}; full-grid cell-by-cell comparison vs independent ground truth`);
})().catch(e => { console.error("TEST FAILURE:", e.message); process.exit(1); });
