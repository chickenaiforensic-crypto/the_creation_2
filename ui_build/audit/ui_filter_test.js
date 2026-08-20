/* Shipped audit harness — full UI functional audit (every control, real user flows). Version: v1.6
   Loads the real app.js with a DOM stub, drives every control the way a user would,
   and cross-checks every observable result against the RAW engine edition files
   (independent code path from build_index.py).

   Coverage: initial state · tournament filter · year filter · player dropdown ·
   find-player autocomplete (typing, keyboard, click, scoping) · Search button
   (exact / unique / none / many) · leaderboard highlight · status banner · Reset.

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
const sortedPlayers = [...truth.allPlayers].sort((a, b) => a.toLowerCase() < b.toLowerCase() ? -1 : 1);
function expectedSuggestions(pool, q) {
  const starts = pool.filter(p => p.toLowerCase().startsWith(q));
  const contains = pool.filter(p => !p.toLowerCase().startsWith(q) && p.toLowerCase().includes(q));
  return [...starts, ...contains].slice(0, 12);
}

/* ---------- minimal DOM stub ---------- */
class El {
  constructor(tag) {
    this.tag = tag; this.children = []; this._listeners = {};
    this._value = ""; this._text = ""; this.innerHTML = ""; this.hidden = false; this.className = "";
  }
  get value() { return this._value; }
  set value(v) { this._value = v; }
  get textContent() { return this._text; }
  set textContent(v) { this._text = v; this.children = []; }
  appendChild(c) { this.children.push(c); return c; }
  addEventListener(ev, fn) { (this._listeners[ev] ??= []).push(fn); }
  dispatch(ev, data) { for (const fn of this._listeners[ev] ?? []) fn(data); }
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
const decode = s => s.replace(/<[^>]*>/g, "")
  .replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">")
  .replace(/&quot;/g, '"').replace(/&#39;/g, "'");

let passed = 0;
function ok(cond, label) { assert.ok(cond, label); passed += 1; }

(async () => {
  await tick(); await tick();

  const tSel = byId["tournament-select"], ySel = byId["year-select"];
  const pSel = byId["player-select"], pInput = byId["player-filter-input"];
  const suggest = byId["player-suggest"], searchBtn = byId["search-btn"];
  const body = byId["matches-body"], count = byId["result-count"];
  const strip = byId["data-strip"], banner = byId["state-banner"], lbBody = byId["leaderboard-body"];

  /* stub-only: seed the static All-tournaments option parsed from index.html */
  const allOpt = new El("option"); allOpt.value = ""; allOpt.textContent = "All tournaments";
  tSel.children.unshift(allOpt);

  /* ---- F1. initial state ---- */
  ok(strip.textContent.includes(`${truth.total.toLocaleString("en-US")} matches`), "F1 data strip");
  ok(tSel.children.length === 1 + Object.keys(truth.byKey).length, "F1 tournament options");
  ok(pSel.children.length === 1 + truth.allPlayers.size, "F1 player options");
  ok(banner.textContent.includes(`${truth.total.toLocaleString("en-US")} matches in scope`), "F1 banner scope count");
  ok(banner.textContent.includes(`${truth.allPlayers.size} players on the leaderboard`), "F1 banner player count");

  /* ---- F2. every tournament: player list + match count vs raw bytes ---- */
  for (const key of Object.keys(truth.byKey)) {
    tSel.value = key; tSel.dispatch("change");
    const exp = [...truth.playersByKey[key]].sort((a, b) => a.toLowerCase() < b.toLowerCase() ? -1 : 1);
    assert.deepStrictEqual(pSel.optionValues().slice(1), exp, `F2 player list ${key}`);
    const n = truth.byKey[key].length;
    assert.strictEqual(count.textContent, `${n.toLocaleString("en-US")} match${n === 1 ? "" : "es"}`, `F2 count ${key}`);
  }

  /* ---- F3. autocomplete: typing suggests names (full scope) ---- */
  tSel.value = ""; tSel.dispatch("change");
  pInput.value = "sin"; pInput.dispatch("input");
  const expSugg = expectedSuggestions(sortedPlayers, "sin");
  ok(expSugg.length > 0 && expSugg.includes("Jannik Sinner"), "F3 ground truth has Sinner");
  const gotSugg = suggest.children.map(li => decode(li.innerHTML));
  assert.deepStrictEqual(gotSugg, expSugg, "F3 suggestion list vs independent computation");
  ok(suggest.hidden === false, "F3 dropdown visible while typing");

  /* ---- F4. keyboard: ArrowDown + Enter selects first suggestion ---- */
  pInput.dispatch("keydown", { key: "ArrowDown", preventDefault() {} });
  pInput.dispatch("keydown", { key: "Enter", preventDefault() {} });
  const chosen = expSugg[0];
  ok(pInput.value === chosen, "F4 input shows chosen player");
  ok(pSel.value === chosen, "F4 dropdown synced to chosen player");
  ok(suggest.hidden === true, "F4 dropdown closed after selection");
  const nChosen = rawMatches.filter(r => r.playerA === chosen || r.playerB === chosen).length;
  assert.strictEqual(count.textContent, `${nChosen.toLocaleString("en-US")} match${nChosen === 1 ? "" : "es"}`, "F4 log filtered to player");
  const hitRows = lbBody.rows().filter(tr => tr.className === "player-hit");
  ok(hitRows.length === 1 && decode(hitRows[0].innerHTML).includes(chosen), "F4 leaderboard row highlighted");
  ok(banner.textContent.includes(`player ${chosen}`), "F4 banner names the player");

  /* ---- F5. suggestions respect tournament scope ---- */
  tSel.value = "Zhengzhou|WTA"; tSel.dispatch("change");
  const zPool = [...truth.playersByKey["Zhengzhou|WTA"]].sort((a, b) => a.toLowerCase() < b.toLowerCase() ? -1 : 1);
  pInput.value = "z"; pInput.dispatch("input");
  const zSugg = suggest.children.map(li => decode(li.innerHTML));
  assert.deepStrictEqual(zSugg, expectedSuggestions(zPool, "z"), "F5 scoped suggestions");
  for (const s of zSugg) ok(truth.playersByKey["Zhengzhou|WTA"].has(s), `F5 ${s} in scope`);

  /* ---- F6. click a suggestion item ---- */
  const clickTarget = zSugg[0];
  const li = suggest.children[0];
  li.dispatch("mousedown", { preventDefault() {} });
  ok(pInput.value === clickTarget && pSel.value === clickTarget, "F6 click selects player");
  const nZ = truth.byKey["Zhengzhou|WTA"].filter(r => r.playerA === clickTarget || r.playerB === clickTarget).length;
  assert.strictEqual(count.textContent, `${nZ.toLocaleString("en-US")} match${nZ === 1 ? "" : "es"}`, "F6 log count after click");

  /* ---- F7. Search button: exact text applies ---- */
  byId["reset-btn"].dispatch("click");
  const exact = sortedPlayers.find(p => p.toLowerCase() === "jannik sinner");
  pInput.value = "Jannik Sinner"; pInput.dispatch("input");
  searchBtn.dispatch("click");
  ok(pSel.value === exact && pInput.value === exact, "F7 exact-name search applied");
  const nS = rawMatches.filter(r => r.playerA === exact || r.playerB === exact).length;
  assert.strictEqual(count.textContent, `${nS.toLocaleString("en-US")} match${nS === 1 ? "" : "es"}`, "F7 log count after search");

  /* ---- F8. Search button: unique partial resolves ---- */
  byId["reset-btn"].dispatch("click");
  const uniq = "Mputde"; // not present — then build a genuine unique partial below
  void uniq;
  const uniquePartial = (() => {
    for (const p of sortedPlayers) {
      const frag = p.slice(0, 5).toLowerCase();
      if (sortedPlayers.filter(x => x.toLowerCase().includes(frag)).length === 1) return { p, frag };
    }
    throw new Error("no unique partial found");
  })();
  pInput.value = uniquePartial.frag; pInput.dispatch("input");
  searchBtn.dispatch("click");
  ok(pSel.value === uniquePartial.p, "F8 unique partial resolved to player");

  /* ---- F9. Search button: no match -> hint, filter untouched ---- */
  byId["reset-btn"].dispatch("click");
  pInput.value = "Zzzqvx"; pInput.dispatch("input");
  searchBtn.dispatch("click");
  ok(pSel.value === "" , "F9 no filter applied on no-match");
  ok(banner.textContent.includes("No player named"), "F9 banner carries no-match hint");
  assert.strictEqual(count.textContent, `${truth.total.toLocaleString("en-US")} matches`, "F9 log still full");

  /* ---- F10. Search button: multiple matches -> guidance, no filter ---- */
  pInput.value = "a"; pInput.dispatch("input");
  searchBtn.dispatch("click");
  ok(pSel.value === "", "F10 ambiguous search does not filter");
  ok(banner.textContent.includes("players match"), "F10 banner asks to pick a suggestion");

  /* ---- F11. full reset proof: everything set, then reset ---- */
  tSel.value = "Basel|ATP"; tSel.dispatch("change");
  ySel.value = "2025"; ySel.dispatch("change");
  pInput.value = "Fonseca"; pInput.dispatch("input");
  searchBtn.dispatch("click");
  ok(pSel.value !== "" && ySel.value === "2025" && tSel.value === "Basel|ATP", "F11 pre-reset state fully set");
  byId["reset-btn"].dispatch("click");
  ok(tSel.value === "", "F11 reset tournament");
  ok(ySel.value === "", "F11 reset year");
  ok(pSel.value === "", "F11 reset player dropdown");
  ok(pInput.value === "", "F11 reset find-player input");
  ok(suggest.hidden === true && suggest.children.length === 0, "F11 reset suggestion box");
  assert.strictEqual(count.textContent, `${truth.total.toLocaleString("en-US")} matches`, "F11 reset log count");
  ok(banner.textContent.includes("all tournaments") && banner.textContent.includes("all years"), "F11 reset banner");
  ok(pSel.children.length === 1 + truth.allPlayers.size, "F11 reset player options");

  console.log(`FULL UI FUNCTIONAL AUDIT PASSED — ${passed} explicit checks + deep-equal grids`);
  console.log(`ground truth: ${truth.total} matches, ${Object.keys(truth.byKey).length} tournaments, ${truth.allPlayers.size} players`);
})().catch(e => { console.error("AUDIT FAILURE:", e.message); process.exit(1); });
