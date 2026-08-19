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
  muteTournaments: [],
  muteYears: [],
  tours: [],
  tournamentFilter: "",
  fromDate: "",
  yearsFrom: "",
  yearsTo: "",
  data: null,
  ratingsPlayer: "",
  ratingsTournament: "",
  ratingsFrom: "",
  ratingsTo: "",
  ratingsData: null,
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
      el("div", { class: "header-right" }, [
        el("span", { class: "version-badge", text: m.app.version }),
        el("div", { class: "dev-lock", text: "Lock: " + m.development_lock.rule }),
      ]),
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

function searchablePlayerInput(m, side) {
  // searchable lookup: free-text input + datalist of every dataset player;
  // choosing an entry loads that player into the side directly
  const isTennis = state.sport === "Tennis";
  const labels = m.entity_labels[state.sport] || {};
  const label = side === "A" ? labels.a_label : (isTennis ? labels.b_label : labels.team_label);
  const wrapper = el("div", { class: "side" });
  wrapper.appendChild(el("label", { text: label }));
  const input = el("input", {
    type: "text",
    list: "players-list",
    placeholder: m.matchup_selector.search_placeholder,
    value: side === "A" ? state.playerA : state.playerB,
  });
  const datalist = el("datalist", { id: "players-list" });
  for (const p of m.options.players) datalist.appendChild(el("option", { value: p }));
  wrapper.appendChild(input);
  wrapper.appendChild(datalist);
  input.addEventListener("change", () => {
    const val = input.value.trim();
    if (!m.options.players.includes(val)) return;
    if (side === "A") state.playerA = val;
    else state.playerB = val;
    loadMatchup();
  });
  return wrapper;
}

function renderMatchupSelector(m) {
  const app = $("#app");
  const labels = m.entity_labels[state.sport] || {};
  const isTennis = state.sport === "Tennis";
  const aLabel = labels.a_label;
  const bLabel = isTennis ? labels.b_label : labels.team_label;

  const panel = el("div", { class: "panel" });
  panel.appendChild(el("h2", { text: isTennis ? aLabel + " vs " + bLabel : m.matchup_selector.team_vs_title }));

  const row = el("div", { class: "matchup-selector" });
  const sideA = searchablePlayerInput(m, "A");
  const swapBtn = el("button", {
    class: "swap-btn",
    title: m.matchup_selector.swap_title,
    text: m.matchup_selector.swap_label + " ⇄",
    onclick: swapPlayers,
  });
  const sideB = searchablePlayerInput(m, "B");
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
    const ratingStr = (p) => (p.system_rating.matches === 0 ? "—" : (p.system_rating.rating > 0 ? "+" : "") + p.system_rating.rating);
    const h2hStr = (p) => (p.h2h.matches === 0 ? "—" : (p.h2h.game_difference > 0 ? "+" : "") + p.h2h.game_difference);
    grid.appendChild(stat(pa.player, ratingStr(pa), ratingCls(pa.system_rating.rating)));
    grid.appendChild(stat(pb.player, ratingStr(pb), ratingCls(pb.system_rating.rating)));
    grid.appendChild(stat(m.h2h_ui.system_rating_prefix + pa.player, h2hStr(pa), ratingCls(pa.h2h.game_difference)));
    grid.appendChild(stat(m.h2h_ui.system_rating_prefix + pb.player, h2hStr(pb), ratingCls(pb.h2h.game_difference)));
  } else {
    grid.appendChild(el("div", { class: "empty", text: m.placeholders.select_players_rating }));
  }
  panel.appendChild(grid);
  if (state.data && state.data.ratings_percentage) {
    const rp = state.data.ratings_percentage;
    const pct = el("div", { class: "h2h-percentage" }, [
      el("div", { class: "k", text: m.ratings_percentage.label + " (" + (state.yearsFrom || "—") + "–" + (state.yearsTo || "—") + ")" }),
    ]);
    if (rp.no_data || rp.pA_pct === null) {
      pct.appendChild(el("div", { class: "empty", text: m.ratings_percentage.no_data_text }));
    } else {
      pct.appendChild(el("div", { class: "pct-row" }, [
        el("span", { class: "pct-a", text: state.data.players.player_a.player + " " + rp.pA_pct + "%" }),
        el("span", { class: "pct-vs", text: " | " }),
        el("span", { class: "pct-b", text: rp.pB_pct + "% " + state.data.players.player_b.player }),
      ]));
    }
    panel.appendChild(pct);
  }
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

    if (h.percentage && h.percentage.pA_pct !== null && h.percentage.pA_pct !== undefined) {
      const pct = el("div", { class: "h2h-percentage" }, [
        el("div", { class: "k", text: ui.percentage_label + " — " + h.direct_encounter_count + " direct" }),
        el("div", { class: "pct-row" }, [
          el("span", { class: "pct-a", text: state.data.players.player_a.player + " " + h.percentage.pA_pct + "%" }),
          el("span", { class: "pct-vs", text: " | " }),
          el("span", { class: "pct-b", text: h.percentage.pB_pct + "% " + state.data.players.player_b.player }),
        ]),
      ]);
      panel.appendChild(pct);
    }

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

function renderTournamentFilter(m) {
  const app = $("#app");
  const panel = el("div", { class: "panel" });
  panel.appendChild(el("h2", { text: m.tournament_filter.label }));
  const row = el("div", { class: "row" });
  const sel = el("select", {
    onchange: (e) => { state.tournamentFilter = e.target.value; loadMatchup(); },
  }, selectOptions(m.all_tournaments, state.tournamentFilter ? [state.tournamentFilter] : [], m.tournament_filter.all_option));
  row.appendChild(sel);
  panel.appendChild(row);
  app.appendChild(panel);
}

function renderDashboard(m) {
  const app = $("#app");
  if (!state.sport) {
    app.appendChild(el("div", { class: "panel", text: m.placeholders.select_sport }));
    return;
  }
  renderTournamentFilter(m);
  renderMatchupSelector(m);
  renderPredictionVector(m);
  const grid = el("div", { class: "grid" });
  grid.appendChild(renderRatingPanel(m));
  grid.appendChild(renderH2HPanel(m));
  app.appendChild(grid);
  app.appendChild(renderPerformancePanel(m));
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
    onchange: (e) => { state.muteYears = [...e.target.selectedOptions].map((o) => o.value); loadMatchup(); },
  }, selectOptions(m.options.years, state.muteYears));
  rowY.appendChild(selY);
  mutePanel.appendChild(rowY);
  const rowT = el("div", { class: "row" });
  rowT.appendChild(el("label", { text: m.mute_ui.mute_tournaments_label }));
  const selT = el("select", {
    multiple: true,
    onchange: (e) => { state.muteTournaments = [...e.target.selectedOptions].map((o) => o.value); loadMatchup(); },
  }, selectOptions(m.options.tournaments, state.muteTournaments));
  rowT.appendChild(selT);
  mutePanel.appendChild(rowT);
  if (m.options.tours.length > 1) {
    const rowR = el("div", { class: "row" });
    rowR.appendChild(el("label", { text: m.mute_ui.tours_label }));
    const selR = el("select", {
      multiple: true,
      onchange: (e) => { state.tours = [...e.target.selectedOptions].map((o) => o.value); loadMatchup(); },
    }, selectOptions(m.options.tours, state.tours));
    rowR.appendChild(selR);
    mutePanel.appendChild(rowR);
  }
  cfgPanel.appendChild(mutePanel);
  app.appendChild(cfgPanel);

  const rangePanel = el("div", { class: "sub-panel" });
  rangePanel.appendChild(el("h3", { text: m.ratings_percentage.range_label }));
  const rangeRow = el("div", { class: "row-inline" });
  const fromWrap = el("div", { class: "row" });
  fromWrap.appendChild(el("label", { text: m.ratings_percentage.from_year_label }));
  const fromSel = el("select", {
    onchange: (e) => { state.yearsFrom = e.target.value; loadMatchup(); },
  }, selectOptions(m.options.years, [state.yearsFrom]));
  fromWrap.appendChild(fromSel);
  const toWrap = el("div", { class: "row" });
  toWrap.appendChild(el("label", { text: m.ratings_percentage.to_year_label }));
  const toSel = el("select", {
    onchange: (e) => { state.yearsTo = e.target.value; loadMatchup(); },
  }, selectOptions(m.options.years, [state.yearsTo]));
  toWrap.appendChild(toSel);
  rangeRow.appendChild(fromWrap);
  rangeRow.appendChild(toWrap);
  rangePanel.appendChild(rangeRow);
  app.appendChild(rangePanel);

  const paramsPanel = el("div", { class: "panel" });
  paramsPanel.appendChild(el("h2", { text: m.configurations.engine_parameters_label }));
  const params = m.configurations.engine_parameters;
  const labels = m.parameters_labels;
  const grid = el("div", { class: "stat-grid" });
  grid.appendChild(stat(labels.points_per_game_difference, params.points_per_game_difference));
  grid.appendChild(stat(labels.feed_tournaments, params.feed_tournaments.join(", ") || "—"));
  grid.appendChild(stat(labels.sports_exposed, params.sports_exposed.join(", ")));
  grid.appendChild(stat(labels.development_lock, params.development_lock_rule));
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
  } else if (state.tab === "ratings") {
    renderRatings(m);
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

function renderPerformancePanel(m) {
  const ui = m.performance;
  const panel = el("div", { class: "panel" });
  panel.appendChild(el("h2", { text: ui.title }));
  if (!state.data || !state.data.players) {
    panel.appendChild(el("div", { class: "empty", text: m.placeholders.select_players_h2h }));
    return panel;
  }
  const pa = state.data.players.player_a.player;
  const pb = state.data.players.player_b.player;
  const grid = el("div", { class: "stat-grid" });
  grid.appendChild(stat(pa, state.performance ? (state.performance.player_a.system_rating > 0 ? "+" : "") + state.performance.player_a.system_rating : "—", ""));
  grid.appendChild(stat(pb, state.performance ? (state.performance.player_b.system_rating > 0 ? "+" : "") + state.performance.player_b.system_rating : "—", ""));
  panel.appendChild(grid);
  if (state.performance) {
    if (state.performance.percentages && state.performance.percentages.length) {
      const pctPanel = el("div", { class: "h2h-percentage" });
      pctPanel.appendChild(el("div", { class: "k", text: ui.percentage_label }));
      for (const p of state.performance.percentages) {
        const row = el("div", { class: "pct-row" }, [
          el("span", { class: "pct-a", text: pa + " " + p.pA_pct + "%" }),
          el("span", { class: "pct-vs", text: " | " + p.tournament + " | " }),
          el("span", { class: "pct-b", text: p.pB_pct + "% " + pb }),
        ]);
        pctPanel.appendChild(row);
      }
      panel.appendChild(pctPanel);
    }
    const windowTable = el("table", {});
    const thead = el("thead", {});
    const headRow = el("tr", {});
    for (const col of ui.window_column_labels) headRow.appendChild(el("th", { text: col }));
    thead.appendChild(headRow);
    windowTable.appendChild(thead);
    const tbody = el("tbody");
    const rows = [];
    const addPlayerWindow = (perf) => {
      for (const res of perf.results) {
        for (const e of res.window) {
          rows.push({
            player: perf.player,
            date: e.date || "—",
            round: e.round || "—",
            opponent: e.opponent || "—",
            score: e.score || "—",
            rating: e.rating,
          });
        }
      }
    };
    addPlayerWindow(state.performance.player_a);
    addPlayerWindow(state.performance.player_b);
    if (rows.length === 0) {
      const tr = el("tr", {});
      tr.appendChild(el("td", { class: "empty", text: ui.no_data_text, colspan: "5" }));
      tbody.appendChild(tr);
    } else {
      for (const r of rows) {
        const tr = el("tr", {}, [
          el("td", { text: r.date }),
          el("td", { text: r.round }),
          el("td", { text: r.opponent }),
          el("td", { text: r.score }),
          el("td", { class: "num", text: (r.rating > 0 ? "+" : "") + r.rating }),
        ]);
        tbody.appendChild(tr);
      }
    }
    windowTable.appendChild(tbody);
    panel.appendChild(el("div", { class: "drilldown-title", text: ui.window_label }));
    panel.appendChild(windowTable);
  }
  return panel;
}

function singlePlayerInput(m) {
  const wrapper = el("div", { class: "side" });
  wrapper.appendChild(el("label", { text: m.ratings.player_label }));
  const input = el("input", {
    type: "text",
    list: "ratings-players-list",
    placeholder: m.matchup_selector.search_placeholder,
    value: state.ratingsPlayer,
  });
  const datalist = el("datalist", { id: "ratings-players-list" });
  for (const p of m.options.players) datalist.appendChild(el("option", { value: p }));
  wrapper.appendChild(input);
  wrapper.appendChild(datalist);
  input.addEventListener("change", () => {
    const val = input.value.trim();
    if (!m.options.players.includes(val)) return;
    state.ratingsPlayer = val;
    state.ratingsData = null;  // stale result invalidated — recompute on Compute
    render();
  });
  return wrapper;
}

function buildRatingsTable(headers, rows) {
  const table = el("table", {});
  const thead = el("thead", {});
  const hr = el("tr", {});
  for (const h of headers) hr.appendChild(el("th", { text: h }));
  thead.appendChild(hr);
  table.appendChild(thead);
  const tbody = el("tbody", {});
  for (const r of rows) {
    const tr = el("tr", {});
    for (const c of r) {
      tr.appendChild(el("td", { class: typeof c === "number" ? "num" : "", text: "" + c }));
    }
    tbody.appendChild(tr);
  }
  table.appendChild(tbody);
  return table;
}

function renderRatings(m) {
  const app = $("#app");
  const ui = m.ratings;

  const panel = el("div", { class: "panel" });
  panel.appendChild(el("h2", { text: ui.title }));
  panel.appendChild(el("p", { class: "muted", text: ui.subtitle }));

  const row = el("div", { class: "matchup-selector" });
  row.appendChild(singlePlayerInput(m));
  const tWrap = el("div", { class: "side" });
  tWrap.appendChild(el("label", { text: ui.tournament_label }));
  tWrap.appendChild(el("select", {
    onchange: (e) => { state.ratingsTournament = e.target.value; state.ratingsData = null; render(); },
  }, selectOptions(m.all_tournaments, state.ratingsTournament ? [state.ratingsTournament] : [], m.tournament_filter.all_option)));
  row.appendChild(tWrap);
  panel.appendChild(row);

  const rangeRow = el("div", { class: "row-inline" });
  const fromWrap = el("div", { class: "row" });
  fromWrap.appendChild(el("label", { text: ui.year_from_label }));
  fromWrap.appendChild(el("select", {
    onchange: (e) => { state.ratingsFrom = e.target.value; state.ratingsData = null; render(); },
  }, selectOptions(m.options.years, [state.ratingsFrom])));
  const toWrap = el("div", { class: "row" });
  toWrap.appendChild(el("label", { text: ui.year_to_label }));
  toWrap.appendChild(el("select", {
    onchange: (e) => { state.ratingsTo = e.target.value; state.ratingsData = null; render(); },
  }, selectOptions(m.options.years, [state.ratingsTo])));
  rangeRow.appendChild(fromWrap);
  rangeRow.appendChild(toWrap);
  panel.appendChild(rangeRow);

  // Compute button — the explicit trigger for the live compute (filters only
  // update state; nothing is computed until this is clicked).
  panel.appendChild(el("button", {
    class: "compute-btn",
    text: ui.compute_label,
    onclick: () => { loadRatings(); },
  }));
  app.appendChild(panel);

  const d = state.ratingsData;
  const result = el("div", { class: "panel" });
  if (!d) {
    result.appendChild(el("div", { class: "empty", text: ui.prompt }));
  } else if (d.matches_rated === 0) {
    result.appendChild(el("div", { class: "empty", text: ui.no_data_text }));
  } else {
    const grid = el("div", { class: "stat-grid" });
    grid.appendChild(stat(ui.total_label, d.rating));
    grid.appendChild(stat(ui.matches_label, d.matches_rated));
    result.appendChild(grid);
    result.appendChild(el("div", { class: "drilldown-title", text: ui.per_year_label }));
    result.appendChild(buildRatingsTable(
      [ui.columns.year, ui.columns.points, ui.columns.matches],
      d.per_year.map((r) => [r.year, r.points, r.matches])
    ));
    result.appendChild(el("div", { class: "drilldown-title", text: ui.per_tournament_label }));
    result.appendChild(buildRatingsTable(
      [ui.columns.tournament, ui.columns.points, ui.columns.matches],
      d.per_tournament.map((r) => [r.tournament, r.points, r.matches])
    ));
    result.appendChild(el("div", { class: "drilldown-title", text: ui.breakdown_title }));
    result.appendChild(buildRatingsTable(
      [ui.columns.date, ui.columns.round, ui.columns.opponent, ui.columns.score, ui.columns.points],
      d.matches.map((r) => [r.date || "—", r.round || "—", r.opponent, r.score || "—", r.points])
    ));
  }
  app.appendChild(result);
}

async function loadRatings() {
  if (!state.ratingsPlayer) return;
  const q = new URLSearchParams({ player: state.ratingsPlayer });
  if (state.ratingsTournament) q.set("tournaments", state.ratingsTournament);
  if (state.ratingsFrom) q.set("years_from", state.ratingsFrom);
  if (state.ratingsTo) q.set("years_to", state.ratingsTo);
  try {
    state.ratingsData = await api("/api/ratings?" + q.toString());
  } catch (e) {
    state.ratingsData = { error: e.message, matches_rated: 0 };
  }
  render();
}

async function loadMatchup() {
  if (!state.playerA || !state.playerB) return;
  const q = new URLSearchParams({ a: state.playerA, b: state.playerB });
  if (state.tournamentFilter) q.set("tournaments", state.tournamentFilter);
  if (state.tours.length) q.set("tours", state.tours.join(","));
  if (state.muteYears.length) q.set("mute_years", state.muteYears.join(","));
  if (state.muteTournaments.length) q.set("mute_tournaments", state.muteTournaments.join(","));
  if (state.fromDate) q.set("from", state.fromDate);
  if (state.yearsFrom) q.set("years_from", state.yearsFrom);
  if (state.yearsTo) q.set("years_to", state.yearsTo);
  try {
    state.data = await api("/api/matchup?" + q.toString());
  } catch (e) {
    state.data = { error: e.message };
  }
  try {
    state.performance = await api("/api/performance?" + q.toString());
  } catch (e) {
    state.performance = null;
  }
  render();
}

(async function init() {
  try {
    state.manifest = await api("/api/ui");
    state.sport = state.manifest.sports[0];
    state.yearsFrom = state.manifest.ratings_percentage.default_from_year;
    state.yearsTo = state.manifest.ratings_percentage.default_to_year;
    render();
  } catch (e) {
    document.getElementById("app").textContent =
      state.manifest.placeholders.load_failed_prefix + e.message;
  }
})();
