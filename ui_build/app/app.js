/* the_creation_2 — blank UI rebuild, Task 1 (tournament + player filter). */
"use strict";

const ROUND_ORDER = { R128: 0, R64: 1, R32: 2, R16: 3, QF: 4, SF: 5, F: 6 };
const RENDER_CAP = 400;

const els = {
  strip: document.getElementById("data-strip"),
  tournament: document.getElementById("tournament-select"),
  playerFilter: document.getElementById("player-filter-input"),
  player: document.getElementById("player-select"),
  reset: document.getElementById("reset-btn"),
  count: document.getElementById("result-count"),
  scope: document.getElementById("scope-note"),
  body: document.getElementById("matches-body"),
  empty: document.getElementById("empty-state"),
  provenance: document.getElementById("provenance"),
};

let INDEX = null;
const state = { tkey: "", player: "", playerQuery: "" };

function tName(tkey) { return tkey.split("|")[0]; }
function tTour(tkey) { return tkey.split("|")[1]; }
function esc(s) {
  return String(s).replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

function fillTournaments() {
  for (const t of INDEX.tournaments) {
    const opt = document.createElement("option");
    opt.value = t.key;
    opt.textContent = `${t.name} — ${t.tour} · ${t.tier} (${t.years[0]}–${t.years[t.years.length - 1]}, ${t.matches} matches)`;
    els.tournament.appendChild(opt);
  }
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

  let keptSelection = false;
  for (const p of list) {
    if (q && !p.toLowerCase().includes(q) && p !== prev) continue;
    const opt = document.createElement("option");
    opt.value = p;
    opt.textContent = p;
    els.player.appendChild(opt);
    if (p === prev) keptSelection = true;
  }
  // Keep an explicitly selected player selectable even if narrowed out by the text filter.
  els.player.value = prev;
}

function filteredMatches() {
  const { tkey, player } = state;
  return INDEX.matches.filter(m =>
    (!tkey || m.tkey === tkey) &&
    (!player || m.playerA === player || m.playerB === player)
  );
}

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

function render() {
  const rows = sortMatches(filteredMatches());
  els.count.textContent = `${rows.length.toLocaleString("en-US")} match${rows.length === 1 ? "" : "es"}`;

  const scopeBits = [];
  if (state.tkey) scopeBits.push(`${tName(state.tkey)} (${tTour(state.tkey)})`);
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

function renderStrip() {
  const p = INDEX.provenance;
  els.strip.textContent =
    `${p.editions_verified} editions · ${p.matches.toLocaleString("en-US")} matches · ` +
    `${INDEX.tournaments.length} tournaments · ${p.distinct_players} players`;
  els.provenance.innerHTML =
    `Data source: engine branch <code>${esc(p.source_branch)}</code> @ <code>${esc(p.source_commit.slice(0, 8))}</code> ` +
    `(content-only pull into <code>ui_build/engine/</code>; no merge). ` +
    `Engine MANIFEST sha256 <code>${esc(p.engine_manifest_sha256.slice(0, 16))}…</code>. ` +
    `${p.editions_verified}/${p.editions_in_manifest} edition files re-verified (sha256 + match count) at index build · built ${esc(p.built_utc)}.`;
}

els.tournament.addEventListener("change", () => {
  state.tkey = els.tournament.value;
  state.playerQuery = "";
  els.playerFilter.value = "";
  rebuildPlayerOptions();
  // Keep the selected player only if they actually play in the new tournament scope.
  if (state.player && state.tkey && !(INDEX.playersByTournament[state.tkey] || []).includes(state.player)) {
    state.player = "";
    els.player.value = "";
  }
  render();
});

els.playerFilter.addEventListener("input", () => {
  state.playerQuery = els.playerFilter.value;
  rebuildPlayerOptions();
});

els.player.addEventListener("change", () => {
  state.player = els.player.value;
  render();
});

els.reset.addEventListener("click", () => {
  state.tkey = ""; state.player = ""; state.playerQuery = "";
  els.tournament.value = "";
  els.playerFilter.value = "";
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
    rebuildPlayerOptions();
    renderStrip();
    render();
  })
  .catch(err => {
    els.strip.textContent = "Failed to load index.json — run ui_build/build_index.py";
    els.count.textContent = String(err);
  });
