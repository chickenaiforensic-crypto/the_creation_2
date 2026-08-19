# WORKORDER — Per-Edition .txt Summaries

**Repo:** chickenaiforensic-crypto/the_creation_2
**Branch:** arena/01a015bb-the-creation-2
**Assigned:** Auditor_1
**Governing rule:** `DATA-RULES.md`, Rule 6

## What's already done

`generate_summaries.py` has been added at `data/tennis/generate_summaries.py` and run once. Every
edition folder now has a `.txt` file alongside its `.json`:

```
data/tennis/editions/Rotterdam/2021.json
data/tennis/editions/Rotterdam/2021.txt
```

Each `.txt` is derived entirely from that edition's own `.json` match data and its
`MANIFEST.json` row — tournament, full tournament name, tier, year, draw size, status, match
count, round coverage, champion/runner-up (read off the Final round's `winner` field), source,
and a truncated checksum. Nothing in a `.txt` file is fetched or asserted beyond what's already
in the `.json`/manifest — it's a rendering, not a new source.

## Your task going forward

Any time you (or anyone) edits an edition's `.json` file or its `MANIFEST.json` row — gap
closures, name corrections, any future fix — regenerate the summaries as part of that same
change:

```
python3 build.py
python3 generate_summaries.py
```

Run `build.py` first. `generate_summaries.py` checks each edition's live match count against
its manifest entry before writing a summary, and will fail loudly if they're out of sync —
that's the signal you forgot to update the manifest checksum/count after an edit.

## Rules

- Never hand-edit a `.txt` file. If a summary looks wrong, the fix belongs in the `.json` or the
  manifest row, then regenerate.
- Do not add new derived fields to the script (e.g. total sets played, longest match) without
  confirming with the Director first — scope creep here just creates another thing that can
  silently drift out of sync.
- If `generate_summaries.py` errors, treat it the same as a `build.py` error: the underlying
  data isn't in a consistent state yet, fix that first.

## Acceptance

For any edition touched in a work session: its `.txt` file's Status/Match count/Checksum lines
match the current `MANIFEST.json` row exactly, and `generate_summaries.py` exits clean with no
errors across all 20 editions.
