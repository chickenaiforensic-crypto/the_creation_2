/* the_creation_2 — blank UI rebuild. Version: v1.4
   Task 1 (tournament + player filter) + Phase 0 Engine Ratings Verification View.

   Phase 0 rating rules (Technical Directive 2026-08-20; implemented here — no
   pre-existing Phase 0 engine ships on this branch):
   - a 7-5 set normalizes down via a -1 reduction to a 6-4 point basis;
   - a 7-6 tiebreak set normalizes directly to a 6-4 point basis;
   - all other physically completed sets count their actual game differential;
   - physically incomplete sets (retirement/default mid-set) are never scored;
   - walkovers carry the literal score "W/O": a counted appearance, zero sets;
   - tier labels are section identifiers only — never mathematical multipliers;
   - any unparseable score token is excluded AND surfaced loudly (audit hook).
*/
"use strict";

const ROUND_ORDER = { R128: 0, R64: 1, R32: 2, R16: 3, QF: 4, SF: 5, F: 6 };
const RENDER_CAP = 400;
const SET_RE = /^(\d+)-(\d+)(\(\d+\))?$/;

const els = {
  strip: document.getElementById("data-strip"),
  tournament: document.getElementById("tournament-select"),
  year: document.getElementById("year-select"),
  playerFilter: document.getElementById("player-filter-input"),
  player: document.getElementById("player-select"),
  reset: document.getElementById("reset-btn"),
  count: document.getElementById("result-count"),
  scope: document.getElementById("scope-note"),
  body: document.getElementById("matches-body"),
  empty: document.getElementById("empty-state"),
  provenance: document.getElementById("provenance"),
  lbMeta: document.getElementById("leaderboard-meta"),
  lbWarn: document.getElementById("leaderboard-warn"),
  lbBody: document.getElementById("leaderboard-body"),
  lbEmpty: document.getElementById("leaderboard-empty"),
};

let INDEX = null;
const state = { tkey: "", year: "", player: "", playerQuery: "" };

/* Version stamp: injected by version.js (kept in sync with ui_build/VERSION).
   File stamp: the served document + shipped file inventory, shown explicitly
   so the preview can always be tied back to repo files. */
const APP_VERSION = (typeof window !== "undefined" && window.APP_VERSION) || "v?";
const DOC_FILE = "index.html";
const SHIPPED_FILES = ["index.html", "app.css", "app.js", "version.js", "index.json"];
(function stampVersion() {
  const badge = document.getElementById("version-badge");
  if (badge) badge.textContent = APP_VERSION;
  const fileBadge = document.getElementById("file-badge");
  if (fileBadge) fileBadge.textContent = DOC_FILE;
  if (typeof document !== "undefined") document.title = `Tennis UI ${APP_VERSION}`;
})();

function tName(tkey) { return tkey.split("|")[0]; }
function tTour(tkey) { return tkey.split("|")[1]; }
function esc(s) {
  return String(s).replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}
function fmtSignedInt(n) { return n > 0 ? `+${n}` : n < 0 ? `-${Math.abs(n)}` : "0"; }
function fmtSignedAvg(x) {
  const s = Math.abs(x).toFixed(1);
  return x > 0 ? `+${s}` : x < 0 ? `-${s}` : "0.0";
}

/* ---------------- Phase 0 ratings math (live, from data) ---------------- */

function isCompleteSet(a, b) {
  const hi = Math.max(a, b), lo = Math.min(a, b);
  return (hi === 6 && lo <= 4) || (hi === 7 && (lo === 5 || lo === 6));
}

function normalizeSet(a, b) {
  /* returns [winnerGames, loserGames] on the mandated point basis */
  const hi = Math.max(a, b), lo = Math.min(a, b);
  if (hi === 7 && (lo === 5 || lo === 6)) return [6, 4]; // 7-5 (-1 reduction), 7-6 tiebreak
  return [hi, lo];
}

function computeRatings(rows) {
  const byPlayer = new Map();
  let unparsedTokens = 0;
  let setsCounted = 0, setsExcludedIncomplete = 0, walkovers = 0;

  const entry = p => {
    let e = byPlayer.get(p);
    if (!e) {
      e = { player: p, rating: 0, matches: 0, bestRoundOrder: -1, champion: false };
      byPlayer.set(p, e);
    }
    return e;
  };

  for (const m of rows) {
    const eA = entry(m.playerA), eB = entry(m.playerB);
    eA.matches += 1; eB.matches += 1;
    for (const p of [m.playerA, m.playerB]) {
      const e = entry(p);
      const order = ROUND_ORDER[m.round] ?? -1;
      if (order > e.bestRoundOrder) e.bestRoundOrder = order;
      if (m.round === "F" && ((m.winner === "A" && p === m.playerA) || (m.winner === "B" && p === m.playerB))) {
        e.champion = true;
      }
    }

    const score = (m.score || "").trim();
    if (score === "W/O") { walkovers += 1; continue; } // appearance, no countable sets
    if (!score) continue;

    const tokens = score.split(/\s+/);
    for (const t of tokens) {
      const mm = SET_RE.exec(t);
      if (!mm) { unparsedTokens += 1; continue; } // audit hook: never silently scored
      const a = parseInt(mm[1], 10), b = parseInt(mm[2], 10);
      if (!isCompleteSet(a, b)) {
        setsExcludedIncomplete += 1; // physically incomplete set: never scored (Phase 0)
        continue;
      }
      const [w, l] = normalizeSet(a, b);
      const diff = w - l;
      if (a > b) { eA.rating += diff; eB.rating -= diff; }
      else { eB.rating += diff; eA.rating -= diff; }
      setsCounted += 1;
    }
  }

  const ROUND_BY_ORDER = Object.fromEntries(Object.entries(ROUND_ORDER).map(([k, v]) => [v, k]));
  const list = [...byPlayer.values()].map(e => ({
    player: e.player,
    rating: e.rating,
    matches: e.matches,
    avg: e.matches > 0 ? e.rating / e.matches : 0,
    bestRound: e.bestRoundOrder >= 0 ? ROUND_BY_ORDER[e.bestRoundOrder] : "—",
    champion: e.champion,
  }));
  list.sort((x, y) => (y.rating - x.rating) || (y.matches - x.matches) || (x.player < y.player ? -1 : x.player > y.player ? 1 : 0));
  list.forEach((e, i) => { e.pos = i + 1; });

  return { list, stats: { setsCounted, setsExcludedIncomplete, walkovers, unparsedTokens } };
}

/* ---------------- filters ---------------- */

function scopeMatches() {
  const { tkey, year } = state;
  return INDEX.matches.filter(m => (!tkey || m.tkey === tkey) && (!year || m.year === year));
}

function tableMatches() {
  const p = state.player;
  return scopeMatches().filter(m => !p || m.playerA === p || m.playerB === p);
}

function fillTournaments() {
  for (const t of INDEX.tournaments) {
    const opt = document.createElement("option");
    opt.value = t.key;
    opt.textContent = `${t.name} — ${t.tour} · ${t.tier} (${t.years[0]}–${t.years[t.years.length - 1]}, ${t.matches} matches)`;
    els.tournament.appendChild(opt);
  }
}

function rebuildYearOptions() {
  const prev = els.year.value;
  const years = new Set();
  if (state.tkey) {
    const t = INDEX.tournaments.find(t => t.key === state.tkey);
    for (const y of (t ? t.years : [])) years.add(y);
  } else {
    for (const m of INDEX.matches) years.add(m.year);
  }
  const sorted = [...years].sort();
  els.year.textContent = "";
  const all = document.createElement("option");
  all.value = "";
  all.textContent = `All years (${sorted.length})`;
  els.year.appendChild(all);
  for (const y of sorted) {
    const opt = document.createElement("option");
    opt.value = y;
    opt.textContent = y;
    els.year.appendChild(opt);
  }
  els.year.value = sorted.includes(prev) ? prev : "";
  state.year = els.year.value;
}

function rebuildPlayerOptions() {
  const list = state.tkey
    ? INDEX.playersByTournament[state.tkey]
    : INDEX.players;
  const q = state.playerQuery.trim().toLowerCase();
  const prev = els.player.value;

  els.player.textContent = "";
  const all = document.createElement("option");
  all.value = "";
  const n = q ? list.filter(p => p.toLowerCase().includes(q)).length : list.length;
  all.textContent = q ? `All players (${n} match the text filter)` : `All players (${list.length})`;
  els.player.appendChild(all);

  for (const p of list) {
    if (q && !p.toLowerCase().includes(q) && p !== prev) continue;
    const opt = document.createElement("option");
    opt.value = p;
    opt.textContent = p;
    els.player.appendChild(opt);
  }
  // Keep an explicitly selected player selectable even if narrowed out by the text filter.
  els.player.value = prev;
}

/* ---------------- rendering ---------------- */

function sortMatches(rows) {
  return rows.slice().sort((a, b) =>
    (a.year === b.year ? 0 : a.year < b.year ? 1 : -1) ||
    ((ROUND_ORDER[a.round] ?? 99) - (ROUND_ORDER[b.round] ?? 99)) ||
    (a.date < b.date ? -1 : a.date > b.date ? 1 : 0)
  );
}

function resultLabel(m) {
  if (m.walkover) return '<span class="badge badge-wo">W.O.</span>';
  if (m.retired) return '<span class="badge badge-ret">RET</span>';
  if (m.defaulted) return '<span class="badge badge-def">DEF</span>';
  return '<span class="muted">completed</span>';
}

function renderLeaderboard() {
  const rows = scopeMatches();
  const { list, stats } = computeRatings(rows);

  const scopeBits = [];
  if (state.tkey) scopeBits.push(`${tName(state.tkey)} (${tTour(state.tkey)})`);
  scopeBits.push(state.year ? `year ${state.year}` : "all years");
  els.lbMeta.textContent =
    `Scope: ${scopeBits.join(" · ")} — ${rows.length.toLocaleString("en-US")} matches · ` +
    `${list.length} players rated · ${stats.setsCounted.toLocaleString("en-US")} sets scored · ` +
    `${stats.setsExcludedIncomplete} incomplete sets excluded · ${stats.walkovers} walkovers (0-set appearances).`;

  if (stats.unparsedTokens > 0) {
    els.lbWarn.hidden = false;
    els.lbWarn.textContent = `AUDIT WARNING: ${stats.unparsedTokens} unparseable score token(s) excluded from ratings — inspect source data.`;
  } else {
    els.lbWarn.hidden = true;
    els.lbWarn.textContent = "";
  }

  els.lbBody.textContent = "";
  const frag = document.createDocumentFragment();
  for (const e of list) {
    const tr = document.createElement("tr");
    const actual = e.champion ? '<span class="champ">CHAMPION</span>' : esc(e.bestRound);
    tr.innerHTML =
      `<td class="mono pos">${e.pos}</td>` +
      `<td>${esc(e.player)}</td>` +
      `<td class="mono ${e.rating > 0 ? "pos-num" : e.rating < 0 ? "neg-num" : ""}">${fmtSignedInt(e.rating)}</td>` +
      `<td class="mono">${e.matches}</td>` +
      `<td class="mono ${e.avg > 0 ? "pos-num" : e.avg < 0 ? "neg-num" : ""}">${fmtSignedAvg(e.avg)}</td>` +
      `<td>${actual}</td>`;
    frag.appendChild(tr);
  }
  els.lbBody.appendChild(frag);
  els.lbEmpty.hidden = list.length > 0;
}

function renderTable() {
  const rows = sortMatches(tableMatches());
  els.count.textContent = `${rows.length.toLocaleString("en-US")} match${rows.length === 1 ? "" : "es"}`;

  const scopeBits = [];
  if (state.tkey) scopeBits.push(`${tName(state.tkey)} (${tTour(state.tkey)})`);
  if (state.year) scopeBits.push(`year ${state.year}`);
  if (state.player) scopeBits.push(state.player);
  els.scope.textContent = scopeBits.length ? `Filtered by: ${scopeBits.join(" · ")}` : "No filters active — full dataset shown.";

  const shown = rows.slice(0, RENDER_CAP);
  els.body.textContent = "";
  const frag = document.createDocumentFragment();

  for (const m of shown) {
    const tr = document.createElement("tr");
    const winnerA = m.winner === "A";
    const pA = `<span class="${winnerA ? "winner" : "loser"}">${esc(m.playerA)}</span>`;
    const pB = `<span class="${!winnerA ? "winner" : "loser"}">${esc(m.playerB)}</span>`;
    tr.innerHTML =
      `<td class="mono">${esc(m.date)}</td>` +
      `<td>${esc(tName(m.tkey))} ${esc(m.year)} <span class="muted">· ${esc(tTour(m.tkey))}</span></td>` +
      `<td>${esc(m.round)}</td>` +
      `<td>${pA} <span class="muted">vs</span> ${pB}</td>` +
      `<td class="mono">${esc(m.score)}</td>` +
      `<td>${resultLabel(m)}</td>`;
    frag.appendChild(tr);
  }
  els.body.appendChild(frag);
  els.empty.hidden = rows.length > 0;

  if (rows.length > shown.length) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td colspan="6" class="muted cap-note">Showing first ${RENDER_CAP} of ${rows.length.toLocaleString("en-US")} filtered matches — refine the filters to narrow further. Counts above remain exact.</td>`;
    els.body.appendChild(tr);
  }
}

function render() { renderLeaderboard(); renderTable(); }

function renderStrip() {
  const p = INDEX.provenance;
  els.strip.textContent =
    `${p.editions_verified} editions · ${p.matches.toLocaleString("en-US")} matches · ` +
    `${INDEX.tournaments.length} tournaments · ${p.distinct_players} players`;
  els.provenance.innerHTML =
    `Data source: engine branch <code>${esc(p.source_branch)}</code> @ <code>${esc(p.source_commit.slice(0, 8))}</code> ` +
    `(content-only pull into <code>ui_build/engine/</code>; no merge). ` +
    `Engine MANIFEST sha256 <code>${esc(p.engine_manifest_sha256.slice(0, 16))}…</code>. ` +
    `${p.editions_verified}/${p.editions_in_manifest} edition files re-verified (sha256 + match count) at index build · built ${esc(p.built_utc)}. ` +
    `Phase 0 ratings computed live in-browser per the 2026-08-20 directive: 7-5 → 6-4 (-1 reduction), 7-6 → 6-4, ` +
    `incomplete sets never scored, tier labels are identifiers only.<br>` +
    `Files: served document <code>ui_build/app/${esc(DOC_FILE)}</code> · shipped ` +
    SHIPPED_FILES.map(f => `<code>${esc(f)}</code>`).join(", ") +
    ` · server <code>ui_build/serve.py</code> · data compiled from ` +
    `<code>ui_build/engine/MANIFEST.json</code> + <code>ui_build/engine/editions/**/*.json</code> ` +
    `(pulled verbatim from the engine branch — see PROVENANCE.md §1).`;
}

/* ---------------- wiring ---------------- */

els.tournament.addEventListener("change", () => {
  state.tkey = els.tournament.value;
  state.playerQuery = "";
  els.playerFilter.value = "";
  rebuildYearOptions();
  rebuildPlayerOptions();
  // Keep the selected player only if they actually play in the new tournament scope.
  if (state.player && state.tkey && !(INDEX.playersByTournament[state.tkey] || []).includes(state.player)) {
    state.player = "";
    els.player.value = "";
  }
  render();
});

els.year.addEventListener("change", () => {
  state.year = els.year.value;
  render();
});

els.playerFilter.addEventListener("input", () => {
  state.playerQuery = els.playerFilter.value;
  rebuildPlayerOptions();
});

els.player.addEventListener("change", () => {
  state.player = els.player.value;
  renderTable();
});

els.reset.addEventListener("click", () => {
  state.tkey = ""; state.year = ""; state.player = ""; state.playerQuery = "";
  els.tournament.value = "";
  els.year.value = ""; // must clear before rebuildYearOptions(), which preserves a still-valid element value
  els.playerFilter.value = "";
  rebuildYearOptions();
  rebuildPlayerOptions();
  els.player.value = "";
  render();
});

fetch("index.json")
  .then(r => {
    if (!r.ok) throw new Error(`index.json HTTP ${r.status}`);
    return r.json();
  })
  .then(idx => {
    INDEX = idx;
    fillTournaments();
    rebuildYearOptions();
    rebuildPlayerOptions();
    renderStrip();
    render();
  })
  .catch(err => {
    els.strip.textContent = "Failed to load index.json — run ui_build/build_index.py";
    els.count.textContent = String(err);
  });
