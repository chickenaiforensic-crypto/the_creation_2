/* Sport Engine SaaS UI — zero-hardcoding frontend.
   Renders entirely from the /api/ui manifest and /api/* engine responses.
   No label, list, or default exists in this file — everything comes from config
   via the API. */

const state = {
  sport: null,
  manifest: null,
  playerA: "",
  playerB: "",
  tournaments: [],
  years: [],
  tours: [],
  fromDate: "",
  data: null,
};

const $ = (sel) => document.querySelector(sel);

async function api(path) {
  const res = await fetch(path);
  if (!res.ok) {
    const body = await res.text();
    throw new Error(body || res.statusText);
  }
  return res.json();
}

function el(tag, attrs = {}, children = []) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") node.className = v;
    else if (k === "text") node.textContent = v;
    else if (k.startsWith("on")) node.addEventListener(k.slice(2), v);
    else node.setAttribute(k, v);
  }
  for (const c of children) node.appendChild(c);
  return node;
}

function selectOptions(values, selected, placeholder) {
  const opts = [];
  if (placeholder !== undefined) {
    opts.push(el("option", { value: "", text: placeholder }));
  }
  for (const v of values) {
    const o = el("option", { value: v, text: v });
    if (selected.includes(v)) o.setAttribute("selected", "");
    opts.push(o);
  }
  return opts;
}

function stat(label, value, cls = "") {
  const v = el("div", { class: "v " + cls, text: value });
  return el("div", { class: "stat" }, [el("div", { class: "k", text: label }), v]);
}

function renderMatchupRow(m) {
  const winner = m.h2h_a > 0 ? m.player_a : m.player_b;
  return el("tr", {}, [
    el("td", { text: m.date || "—" }),
    el("td", { text: m.player_a }),
    el("td", { text: m.player_b }),
    el("td", { text: m.score || "—" }),
    el("td", { class: "num", text: (m.h2h_a || 0) + "" }),
    el("td", { class: "num", text: (m.h2h_b || 0) + "" }),
    el("td", { text: winner }),
  ]);
}

function render() {
  const app = $("#app");
  const m = state.manifest;
  app.innerHTML = "";

  // Header
  app.appendChild(
    el("header", { class: "app-header" }, [
      el("div", {}, [
        el("h1", { text: m.app.name }),
        el("p", { text: m.app.slogan }),
      ]),
      el("div", { class: "dev-lock", text: "Lock: " + m.development_lock.rule }),
    ])
  );

  // Sports selector
  const sportsBar = el("div", { class: "sports-bar" });
  for (const sport of m.sports) {
    const locked = !m.development_lock.exposed_sports.includes(sport);
    const btn = el("button", {
      text: sport,
      disabled: locked ? "" : undefined,
      class: state.sport === sport ? "active" : "",
      onclick: () => {
        state.sport = sport;
        state.playerA = state.playerB = "";
        render();
      },
    });
    sportsBar.appendChild(btn);
  }
  app.appendChild(sportsBar);

  if (!state.sport) {
    app.appendChild(el("div", { class: "panel", text: "Select a sport to begin." }));
    return;
  }

  const labels = m.entity_labels[state.sport] || {};
  const isTennis = state.sport === "Tennis";

  // Matchup selector
  const selector = el("div", { class: "panel" });
  selector.appendChild(el("h2", { text: isTennis ? "Player A vs Player B" : "Team A vs Team B" }));
  const rowA = el("div", { class: "row" });
  rowA.appendChild(el("label", { text: labels.a_label }));
  const selA = el("select", {
    onchange: (e) => { state.playerA = e.target.value; loadMatchup(); },
  }, selectOptions(m.options.players, [state.playerA], "— select " + labels.a_label + " —"));
  rowA.appendChild(selA);
  selector.appendChild(rowA);
  const rowB = el("div", { class: "row" });
  rowB.appendChild(el("label", { text: isTennis ? labels.b_label : labels.team_label }));
  const selB = el("select", {
    onchange: (e) => { state.playerB = e.target.value; loadMatchup(); },
  }, selectOptions(m.options.players, [state.playerB], "— select " + (isTennis ? labels.b_label : labels.team_label) + " —"));
  rowB.appendChild(selB);
  selector.appendChild(rowB);
  app.appendChild(selector);

  // Mute block
  const mute = el("div", { class: "panel" });
  mute.appendChild(el("h2", { text: m.mute_ui.label }));
  const rowY = el("div", { class: "row" });
  rowY.appendChild(el("label", { text: m.mute_ui.mute_years_label }));
  const selY = el("select", { multiple: true, onchange: (e) => {
    state.years = [...e.target.selectedOptions].map((o) => o.value); loadMatchup();
  } }, selectOptions(m.options.years, state.years));
  rowY.appendChild(selY);
  mute.appendChild(rowY);
  const rowT = el("div", { class: "row" });
  rowT.appendChild(el("label", { text: m.mute_ui.mute_tournaments_label }));
  const selT = el("select", { multiple: true, onchange: (e) => {
    state.tournaments = [...e.target.selectedOptions].map((o) => o.value); loadMatchup();
  } }, selectOptions(m.options.tournaments, state.tournaments));
  rowT.appendChild(selT);
  mute.appendChild(rowT);
  if (m.options.tours.length > 1) {
    const rowR = el("div", { class: "row" });
    rowR.appendChild(el("label", { text: "Tour" }));
    const selR = el("select", { multiple: true, onchange: (e) => {
      state.tours = [...e.target.selectedOptions].map((o) => o.value); loadMatchup();
    } }, selectOptions(m.options.tours, state.tours));
    rowR.appendChild(selR);
    mute.appendChild(rowR);
  }
  app.appendChild(mute);

  // H2H date boundary
  const h2hPanel = el("div", { class: "panel" });
  h2hPanel.appendChild(el("h2", { text: m.h2h_ui.title }));
  const rowD = el("div", { class: "row" });
  rowD.appendChild(el("label", { text: m.h2h_ui.date_boundary_label }));
  const dateInput = el("input", {
    type: "date",
    value: state.fromDate,
    onchange: (e) => { state.fromDate = e.target.value; loadMatchup(); },
  });
  rowD.appendChild(dateInput);
  h2hPanel.appendChild(rowD);
  app.appendChild(h2hPanel);

  // Master stat: prediction vector (zeroed placeholder)
  const vector = el("div", { class: "vector zeroed" }, [
    el("div", { class: "side pA", text: state.data ? (state.data.prediction_vector.pA === null ? "—" : state.data.prediction_vector.pA + "%") : "—" }),
    el("div", { class: "vs", text: "vs" }),
    el("div", { class: "side pB", text: state.data ? (state.data.prediction_vector.pB === null ? "—" : state.data.prediction_vector.pB + "%") : "—" }),
  ]);
  app.appendChild(vector);
  const vnote = el("div", { class: "vector-note", text: m.prediction_vector.zeroed_state_text });
  app.appendChild(vnote);

  // Results
  const results = el("div", { class: "grid" });

  // System rating
  const ratingPanel = el("div", { class: "panel" });
  ratingPanel.appendChild(el("h2", { text: m.system_rating_label }));
  const ratingGrid = el("div", { class: "stat-grid" });
  if (state.data && state.data.players) {
    const pa = state.data.players.player_a;
    const pb = state.data.players.player_b;
    ratingGrid.appendChild(stat(pa.player, (pa.system_rating.rating > 0 ? "+" : "") + pa.system_rating.rating, pa.system_rating.rating > 0 ? "pos" : pa.system_rating.rating < 0 ? "neg" : ""));
    ratingGrid.appendChild(stat(pb.player, (pb.system_rating.rating > 0 ? "+" : "") + pb.system_rating.rating, pb.system_rating.rating > 0 ? "pos" : pb.system_rating.rating < 0 ? "neg" : ""));
    const net = pa.h2h.game_difference - pb.h2h.game_difference;
    ratingGrid.appendChild(stat("H2H game diff " + pa.player, (pa.h2h.game_difference > 0 ? "+" : "") + pa.h2h.game_difference, pa.h2h.game_difference > 0 ? "pos" : pa.h2h.game_difference < 0 ? "neg" : ""));
    ratingGrid.appendChild(stat("H2H game diff " + pb.player, (pb.h2h.game_difference > 0 ? "+" : "") + pb.h2h.game_difference, pb.h2h.game_difference > 0 ? "pos" : pb.h2h.game_difference < 0 ? "neg" : ""));
  } else {
    ratingGrid.appendChild(el("div", { class: "empty", text: "Select two players to see system ratings." }));
  }
  ratingPanel.appendChild(ratingGrid);
  results.appendChild(ratingPanel);

  // H2H analysis summation + drill-down
  const h2hResults = el("div", { class: "panel" });
  h2hResults.appendChild(el("h2", { text: m.h2h_ui.summary_label }));
  if (state.data && state.data.h2h) {
    const h = state.data.h2h;
    const bar = el("div", { class: "h2h-bar" }, [
      el("div", { class: "stat", }, [
        el("div", { class: "k", text: "Net H2H balance" }),
        el("div", { class: "v " + (h.net_h2h_balance > 0 ? "pos" : h.net_h2h_balance < 0 ? "neg" : ""), text: (h.net_h2h_balance > 0 ? "+" : "") + h.net_h2h_balance }),
      ]),
      el("button", { class: "icon-btn", text: "⤓ H2H drill-down (" + h.encounter_count + ")", onclick: toggleDrilldown }),
    ]);
    h2hResults.appendChild(bar);
    const dd = el("div", { id: "drilldown", style: "display:none" });
    const table = el("table", {}, [
      el("thead", {}, [el("tr", {}, ["Date", "A", "B", "Score", "H2H A", "H2H B", "Winner"].map((t) => el("th", { text: t })))]),
    ]);
    const tbody = el("tbody");
    if (h.encounters.length === 0) {
      tbody.appendChild(el("tr", {}, [el("td", { class: "empty", text: h.no_data_text, colspan: "7" })]));
    } else {
      for (const mrow of h.encounters) tbody.appendChild(renderMatchupRow(mrow));
    }
    table.appendChild(tbody);
    dd.appendChild(table);
    h2hResults.appendChild(dd);
  } else {
    h2hResults.appendChild(el("div", { class: "empty", text: "Select two players to see H2H." }));
  }
  results.appendChild(h2hResults);
  app.appendChild(results);
}

function toggleDrilldown() {
  const dd = document.getElementById("drilldown");
  if (dd) dd.style.display = dd.style.display === "none" ? "block" : "none";
}

async function loadMatchup() {
  if (!state.playerA || !state.playerB) return;
  const q = new URLSearchParams({ a: state.playerA, b: state.playerB });
  if (state.years.length) q.set("years", state.years.join(","));
  if (state.tournaments.length) q.set("tournaments", state.tournaments.join(","));
  if (state.tours.length) q.set("tours", state.tours.join(","));
  if (state.fromDate) q.set("from", state.fromDate);
  try {
    state.data = await api("/api/matchup?" + q.toString());
  } catch (e) {
    state.data = { error: e.message };
  }
  render();
}

(async function init() {
  try {
    state.manifest = await api("/api/ui");
    state.sport = state.manifest.sports[0];
    render();
  } catch (e) {
    document.getElementById("app").textContent = "Failed to load UI manifest: " + e.message;
  }
})();
