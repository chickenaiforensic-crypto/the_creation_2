#!/usr/bin/env python3
"""
verify_data.py — production data verifier for the_creation_2.

Verifies the manifest-selected active store (and pinned verification targets)
against the artifact bytes. Structural checks are derived from the audit
standard established by T-002 (Auditor 1, Director-verified 2026-08-18).

Usage (from the repository root):
    python3 Engineering/tools/verify_data.py
    python3 Engineering/tools/verify_data.py --json
    python3 Engineering/tools/verify_data.py --store <path>   # explicit forensic check
    python3 Engineering/tools/verify_data.py --manifest <path>

Exit status: 0 = every implemented check reproduced from disk;
             1 = at least one check failed.
"""

import argparse
import hashlib
import json
import os
import re
import sys

ROUND_ORDER = ['R128', 'R64', 'R32', 'R16', 'QF', 'SF', 'F']


def md5_of(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def find_repo_root(start):
    d = os.path.abspath(start)
    while True:
        for rel in ('data/MANIFEST.json', 'data/Data_Sports/data/MANIFEST.json'):
            if os.path.isfile(os.path.join(d, rel)):
                return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


class Checker:
    def __init__(self):
        self.checks = []  # (name, ok, detail)

    def check(self, name, ok, detail=''):
        self.checks.append((name, bool(ok), detail))


def verify_store(path, pin_rows, pin_md5, pin_sha256, c):
    c.check('store exists', os.path.isfile(path), path)
    if not os.path.isfile(path):
        return None
    m_md5, m_sha = md5_of(path), sha256_of(path)
    c.check('store md5 matches pin', m_md5 == pin_md5, f'{m_md5} vs {pin_md5}')
    c.check('store sha256 matches pin', m_sha == pin_sha256, f'{m_sha[:16]}… vs {pin_sha256[:16]}…')
    try:
        with open(path) as f:
            data = json.load(f)
    except Exception as e:
        c.check('store parses as JSON', False, str(e))
        return None
    c.check('store parses as JSON', True)
    rows = data.get('matches')
    count = data.get('count')
    c.check('count == len(matches)', count == len(rows), f'{count} vs {len(rows)}')
    c.check('row count matches pin', len(rows) == pin_rows, f'{len(rows)} vs {pin_rows}')
    if rows is None:
        return None

    # ---- structural checks (T-002 standard) ----
    n_arith = n_dup = n_byte_dup = n_self = n_flag = n_marker = n_winner = 0
    n_null_tag = n_tag_date = n_no_prov = 0
    seen = set()
    bytes_seen = set()
    score_re = re.compile(r'^(\d+)-(\d+)$')
    for r in rows:
        # duplicates: per-edition composite key + byte-identical rows
        key = (r.get('tournament'), r.get('tour'), r.get('edition_year'), r.get('round'),
               r.get('playerA'), r.get('playerB'))
        if key in seen:
            n_dup += 1
        seen.add(key)
        rb = json.dumps(r, sort_keys=True)
        if rb in bytes_seen:
            n_byte_dup += 1
        bytes_seen.add(rb)
        # self-play
        if r.get('playerA') == r.get('playerB'):
            n_self += 1
        # winner convention
        if r.get('winner') != 'A':
            n_winner += 1
        # score markers must be absent (T-003 D3 policy)
        sc = r.get('score', '')
        if 'RET' in sc or 'Def.' in sc or ' DEF' in sc:
            n_marker += 1
        # status <-> flag coherence
        st = r.get('status')
        if st == 'retired' and not r.get('retired'):
            n_flag += 1
        if st == 'walkover' and not r.get('walkover'):
            n_flag += 1
        if st == 'defaulted' and not r.get('defaulted'):
            n_flag += 1
        if st == 'completed' and (r.get('retired') or r.get('walkover') or r.get('defaulted')):
            n_flag += 1
        if st not in ('completed', 'retired', 'walkover', 'defaulted'):
            n_flag += 1
        # forensic-null tagging: date == '' iff provenance.forensic_null == True
        has_null = (r.get('date') == '')
        tagged = bool((r.get('provenance') or {}).get('forensic_null'))
        if has_null != tagged:
            n_null_tag += 1
        # provenance + source presence
        if not r.get('provenance') or not r.get('source'):
            n_no_prov += 1
        # score arithmetic: winner games/sets sums vs score pairs
        try:
            pairs = []
            for tok in sc.split():
                tok = tok.split('(')[0]
                m2 = score_re.match(tok)
                if m2:
                    pairs.append((int(m2.group(1)), int(m2.group(2))))
            if pairs:
                gA = sum(p[0] for p in pairs)
                gB = sum(p[1] for p in pairs)
                sA = sum(1 for p in pairs if p[0] > p[1])
                sB = sum(1 for p in pairs if p[1] > p[0])
                if int(r.get('gamesA', -1)) != gA or int(r.get('gamesB', -1)) != gB:
                    n_arith += 1
                if int(r.get('setsA', -1)) != sA or int(r.get('setsB', -1)) != sB:
                    n_arith += 1
        except (TypeError, ValueError):
            n_arith += 1

    c.check('0 duplicate (edition, round, playerA, playerB) keys', n_dup == 0, f'{n_dup} found')
    c.check('0 byte-identical rows', n_byte_dup == 0, f'{n_byte_dup} found')
    c.check('0 self-play rows', n_self == 0, f'{n_self} found')
    c.check('winner == "A" on all rows', n_winner == 0, f'{n_winner} violations')
    c.check('0 score-marker tokens (T-003 D3 policy)', n_marker == 0, f'{n_marker} found')
    c.check('0 status<->flag incoherences', n_flag == 0, f'{n_flag} found')
    c.check('forensic-null tag <-> empty date correspondence', n_null_tag == 0, f'{n_null_tag} mismatches')
    c.check('provenance + source on every row', n_no_prov == 0, f'{n_no_prov} missing')
    c.check('score arithmetic vs gamesA/gamesB/setsA/setsB', n_arith == 0, f'{n_arith} mismatches')

    # ---- per-edition structure ----
    editions = {}
    for r in rows:
        editions.setdefault((r.get('tournament'), r.get('tour'), r.get('edition_year')), []).append(r)
    gs_short = bracket_bad = gs_count = 0
    for (tn, tour, yr), ers in editions.items():
        if ers and ers[0].get('tier') == 'GS':
            gs_count += 1
            # GS edition: 127-row census (KNOWN-GAPS §1)
            if len(ers) != 127:
                gs_short += 1
            # strict bracket progression, both directions
            for a, b in zip(ROUND_ORDER, ROUND_ORDER[1:]):
                ra = [r for r in ers if r.get('round') == a]
                rb = [r for r in ers if r.get('round') == b]
                if ra and rb:
                    wa = {r.get('playerA') for r in ra}
                    pb = {p for r in rb for p in (r.get('playerA'), r.get('playerB'))}
                    if wa != pb:
                        bracket_bad += 1
    c.check('all 46 GS editions hold 127 rows', gs_short == 0 and gs_count == 46, f'{gs_count} GS editions, {gs_short} short')
    c.check('bracket progression (both directions) holds on all GS editions', bracket_bad == 0, f'{bracket_bad} breaks')
    c.check('edition census', True, f'{len(editions)} editions across {len(rows)} rows')
    return data


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--json', action='store_true', help='machine-readable output')
    ap.add_argument('--manifest', help='explicit path to MANIFEST.json (forensic checks)')
    ap.add_argument('--store', help='explicit path to a store file (forensic checks)')
    args = ap.parse_args()

    root = find_repo_root(os.getcwd())
    manifest_path = args.manifest or (os.path.join(root, 'data', 'MANIFEST.json') if root else None)
    if not manifest_path or not os.path.isfile(manifest_path):
        print('ERROR: MANIFEST.json not found; run from the repository root or pass --manifest.')
        sys.exit(1)

    with open(manifest_path) as f:
        manifest = json.load(f)
    base = os.path.dirname(manifest_path)

    c = Checker()
    active = manifest.get('active_store', {})
    store_path = args.store or os.path.join(base, active.get('path', ''))
    verify_store(store_path, active.get('rows', -1), active.get('md5', ''), active.get('sha256', ''), c)

    # verification targets (football)
    for sport, tgt in (manifest.get('verification_targets') or {}).items():
        tp = os.path.join(base, tgt.get('path', ''))
        c.check(f'{sport} verification target md5', md5_of(tp) == tgt.get('md5', ''), tp)
        c.check(f'{sport} verification target sha256', sha256_of(tp) == tgt.get('sha256', ''), tp)

    # canonical names table
    cn = manifest.get('canonical_names', {})
    if cn:
        tp = os.path.join(base, cn.get('path', ''))
        ok_dig = md5_of(tp) == cn.get('md5', '') and sha256_of(tp) == cn.get('sha256', '')
        entries = None
        if ok_dig:
            try:
                with open(tp) as f:
                    entries = len(json.load(f))
            except Exception:
                entries = None
        c.check('canonical names table digests', ok_dig, tp)
        c.check('canonical names table entries', entries == cn.get('entries', -1), f'{entries} vs {cn.get("entries")}')

    failed = [x for x in c.checks if not x[1]]
    if args.json:
        out = {'exit': 0 if not failed else 1,
               'checks': [{'name': n, 'ok': ok, 'detail': d} for n, ok, d in c.checks]}
        print(json.dumps(out, indent=2))
    else:
        for name, ok, detail in c.checks:
            mark = 'PASS' if ok else 'FAIL'
            extra = f' — {detail}' if detail else ''
            print(f'[{mark}] {name}{extra}')
        print(f'\n{"ALL CHECKS PASSED" if not failed else f"{len(failed)} CHECK(S) FAILED"}')

    sys.exit(0 if not failed else 1)


if __name__ == '__main__':
    main()
