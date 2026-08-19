/* Sport Engine SaaS UI — zero-hardcoding frontend.
   Renders entirely from the /api/ui manifest and /api/* engine responses.
   No label, list, or default exists in this file — everything comes from config
   via the API. */

const state = {
  sport: null,
  tab: "dashboard",
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

function renderMatchupRow(m, cols) {
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

function renderHeader(m) {
  const app = $("#app");
  app.appendChild(
    el("header", { class: "app-header" }, [
      el("div", {}, [
        el("h1", { text: m.app.name }),
        el("p", { text: m.app.slogan }),
      ]),
      el("div", { class: "dev-lock", text: "Lock: " + m.development_lock.rule }),
    ])
  );
}

function renderSportsBar(m) {
  const app = $("#app");
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
        state.data = null;
        render();
      },
    });
    sportsBar.appendChild(btn);
  }
  app.appendChild(sportsBar);
}

function renderTabs(m) {
  const app = $("#app");
  const bar = el("div", { class: "tabs-bar" });
  for (const [key, label] of Object.entries(m.tabs)) {
    if (key === "system_configurations_label" || key === "engine_parameters_label") continue;
    const btn = el("button", {
      class: "tab-btn" + (state.tab === key ? " active" : ""),
      text: label,
      onclick: () => { state.tab = key; render(); },
    });
    bar.appendChild(btn);
  }
  app.appendChild(bar);
}

function renderMatchupSelector(m) {
  const app = $("#app");
  const labels = m.entity_labels[state.sport] || {};
  const isTennis = state.sport === "Tennis";
  const aLabel = labels.a_label;
  const bLabel = isTennis ? labels.b_label : labels.team_label;
  const prefix = m.matchup_selector.select_prefix;

  const panel = el("div", { class: "panel" });
  panel.appendChild(el("h2", { text: isTennis ? aLabel + " vs " + bLabel : "Team A vs Team B" }));

  const row = el("div", { class: "matchup-selector" });

  const sideA = el("div", { class: "side" });
  sideA.appendChild(el("label", { text: aLabel }));
  const selA = el("select", {
    id: "selA",
    onchange: (e) => { state.playerA = e.target.value; loadMatchup(); },
  }, selectOptions(m.options.players, [state.playerA], prefix + " " + aLabel + " —"));
  sideA.appendChild(selA);

  const swapBtn = el("button", {
    class: "swap-btn",
    title: m.matchup_selector.swap_title,
    text: m.matchup_selector.swap_label + " ⇄",
    onclick: swapPlayers,
  });

  const sideB = el("div", { class: "side" });
  sideB.appendChild(el("label", { text: bLabel }));
  const selB = el("select", {
    id: "selB",
    onchange: (e) => { state.playerB = e.target.value; loadMatchup(); },
  }, selectOptions(m.options.players, [state.playerB], prefix + " " + bLabel + " —"));
  sideB.appendChild(selB);

  row.appendChild(sideA);
  row.appendChild(swapBtn);
  row.appendChild(sideB);
  panel.appendChild(row);
  app.appendChild(panel);
}

function renderPredictionVector(m) {
  const app = $("#app");
  const v = m.prediction_vector;
  const d = state.data;
  const pA = d && d.prediction_vector ? (d.prediction_vector.pA === null ? "—" : d.prediction_vector.pA + "%") : "—";
  const pB = d && d.prediction_vector ? (d.prediction_vector.pB === null ? "—" : d.prediction_vector.pB + "%") : "—";
  app.appendChild(
    el("div", { class: "vector zeroed" }, [
      el("div", { class: "side pA", text: pA }),
      el("div", { class: "vs", text: v.vs_label }),
      el("div", { class: "side pB", text: pB }),
    ])
  );
  app.appendChild(el("div", { class: "vector-note", text: v.zeroed_state_text }));
}

function renderRatingPanel(m) {
  const panel = el("div", { class: "panel" });
  panel.appendChild(el("h2", { text: m.system_rating_label }));
  const grid = el("div", { class: "stat-grid" });
  if (state.data && state.data.players) {
    const pa = state.data.players.player_a;
    const pb = state.data.players.player_b;
    const ratingCls = (r) => (r > 0 ? "pos" : r < 0 ? "neg" : "");
    grid.appendChild(stat(pa.player, (pa.system_rating.rating > 0 ? "+" : "") + pa.system_rating.rating, ratingCls(pa.system_rating.rating)));
    grid.appendChild(stat(pb.player, (pb.system_rating.rating > 0 ? "+" : "") + pb.system_rating.rating, ratingCls(pb.system_rating.rating)));
    grid.appendChild(stat("H2H " + pa.player, (pa.h2h.game_difference > 0 ? "+" : "") + pa.h2h.game_difference, ratingCls(pa.h2h.game_difference)));
    grid.appendChild(stat("H2H " + pb.player, (pb.h2h.game_difference > 0 ? "+" : "") + pb.h2h.game_difference, ratingCls(pb.h2h.game_difference)));
  } else {
    grid.appendChild(el("div", { class: "empty", text: m.placeholders.select_players_rating }));
  }
  panel.appendChild(grid);
  return panel;
}

function renderH2HPanel(m) {
  const ui = m.h2h_ui;
  const panel = el("div", { class: "panel" });
  panel.appendChild(el("h2", { text: ui.title }));

  const rowD = el("div", { class: "row" });
  rowD.appendChild(el("label", { text: ui.date_boundary_label }));
  const dateInput = el("input", {
    type: "date",
    value: state.fromDate,
    onchange: (e) => { state.fromDate = e.target.value; loadMatchup(); },
  });
  rowD.appendChild(dateInput);
  panel.appendChild(rowD);

  if (state.data && state.data.h2h) {
    const h = state.data.h2h;
    const bar = el("div", { class: "h2h-bar" }, [
      el("div", { class: "stat" }, [
        el("div", { class: "k", text: ui.summary_label }),
        el("div", { class: "v " + (h.net_h2h_balance > 0 ? "pos" : h.net_h2h_balance < 0 ? "neg" : ""), text: (h.net_h2h_balance > 0 ? "+" : "") + h.net_h2h_balance }),
      ]),
      el("button", {
        class: "icon-btn",
        title: ui.drilldown_icon_label,
        text: ui.drilldown_button_label + " (" + h.encounter_count + ")",
        onclick: toggleDrilldown,
      }),
    ]);
    panel.appendChild(bar);

    const dd = el("div", { id: "drilldown", style: "display:none" });
    dd.appendChild(el("div", { class: "drilldown-title", text: ui.score_sheet_title }));
    const table = el("table", {});
    const thead = el("thead", {});
    const headRow = el("tr", {});
    for (const key of ["date", "player_a", "player_b", "score", "h2h_a", "h2h_b", "winner"]) {
      headRow.appendChild(el("th", { text: ui.columns[key] }));
    }
    thead.appendChild(headRow);
    table.appendChild(thead);
    const tbody = el("tbody");
    if (h.encounters.length === 0) {
      const tr = el("tr", {});
      tr.appendChild(el("td", { class: "empty", text: h.no_data_text, colspan: "7" }));
      tbody.appendChild(tr);
    } else {
      for (const mrow of h.encounters) tbody.appendChild(renderMatchupRow(mrow, ui.columns));
    }
    table.appendChild(tbody);
    dd.appendChild(table);
    panel.appendChild(dd);
  } else {
    panel.appendChild(el("div", { class: "empty", text: m.placeholders.select_players_h2h }));
  }
  return panel;
}

function renderDashboard(m) {
  const app = $("#app");
  if (!state.sport) {
    app.appendChild(el("div", { class: "panel", text: m.placeholders.select_sport }));
    return;
  }
  renderMatchupSelector(m);
  renderPredictionVector(m);
  const grid = el("div", { class: "grid" });
  grid.appendChild(renderRatingPanel(m));
  grid.appendChild(renderH2HPanel(m));
  app.appendChild(grid);
}

function renderConfigurations(m) {
  const app = $("#app");
  const cfgPanel = el("div", { class: "panel" });
  cfgPanel.appendChild(el("h2", { text: m.configurations.system_configurations_label }));

  const mutePanel = el("div", { class: "sub-panel" });
  mutePanel.appendChild(el("h3", { text: m.mute_ui.label }));
  const rowY = el("div", { class: "row" });
  rowY.appendChild(el("label", { text: m.mute_ui.mute_years_label }));
  const selY = el("select", {
    multiple: true,
    onchange: (e) => { state.years = [...e.target.selectedOptions].map((o) => o.value); loadMatchup(); },
  }, selectOptions(m.options.years, state.years));
  rowY.appendChild(selY);
  mutePanel.appendChild(rowY);
  const rowT = el("div", { class: "row" });
  rowT.appendChild(el("label", { text: m.mute_ui.mute_tournaments_label }));
  const selT = el("select", {
    multiple: true,
    onchange: (e) => { state.tournaments = [...e.target.selectedOptions].map((o) => o.value); loadMatchup(); },
  }, selectOptions(m.options.tournaments, state.tournaments));
  rowT.appendChild(selT);
  mutePanel.appendChild(rowT);
  if (m.options.tours.length > 1) {
    const rowR = el("div", { class: "row" });
    rowR.appendChild(el("label", { text: m.mute_ui.mute_tours_label }));
    const selR = el("select", {
      multiple: true,
      onchange: (e) => { state.tours = [...e.target.selectedOptions].map((o) => o.value); loadMatchup(); },
    }, selectOptions(m.options.tours, state.tours));
    rowR.appendChild(selR);
    mutePanel.appendChild(rowR);
  }
  cfgPanel.appendChild(mutePanel);
  app.appendChild(cfgPanel);

  const paramsPanel = el("div", { class: "panel" });
  paramsPanel.appendChild(el("h2", { text: m.configurations.engine_parameters_label }));
  const params = m.configurations.engine_parameters;
  const grid = el("div", { class: "stat-grid" });
  grid.appendChild(stat("Points per game difference", params.points_per_game_difference));
  grid.appendChild(stat("Feed tournaments", params.feed_tournaments.join(", ") || "—"));
  grid.appendChild(stat("Sports exposed", params.sports_exposed.join(", ")));
  grid.appendChild(stat("Development lock", params.development_lock_rule));
  paramsPanel.appendChild(grid);
  app.appendChild(paramsPanel);
}

function render() {
  const app = $("#app");
  const m = state.manifest;
  app.innerHTML = "";
  renderHeader(m);
  renderSportsBar(m);
  renderTabs(m);
  if (state.tab === "configurations") {
    renderConfigurations(m);
  } else {
    renderDashboard(m);
  }
}

function toggleDrilldown() {
  const dd = document.getElementById("drilldown");
  if (dd) dd.style.display = dd.style.display === "none" ? "block" : "none";
}

function swapPlayers() {
  if (!state.playerA && !state.playerB) return;
  const tmp = state.playerA;
  state.playerA = state.playerB;
  state.playerB = tmp;
  loadMatchup();
  render();
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
    document.getElementById("app").textContent =
      state.manifest.placeholders.load_failed_prefix + e.message;
  }
})();
