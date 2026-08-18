# Production data — manifest-selected single source of truth

`data/` is the production data tree (absolute path: `data/` in the repository
root). Store selection is controlled by
[`MANIFEST.json`](MANIFEST.json); applications and verification tools must not hardcode a
store filename. All manifest paths resolve against this root; football checksums are
pinned at `football/checksums.json` (digests identical to the manifest verification
target).

## Structure

```text
data/
├── MANIFEST.json       active-store, verification-target, and canonical-names configuration
├── football/           football store, approval card, checksums, and known gaps
└── tennis/             canonical tennis SSoT, PIN, names, approval card, and known gaps
```

Historical verification batches, one-shot migration scripts, transaction manifests, and
custody records live under the top-level `quarantine/evidence/` tree — never under `data/`.
(Note: this checkout contains no `quarantine/evidence/` directory; that history lives on
the predecessor-project branches referenced by `tennis/PIN.txt`. No quarantined artifact
is present in this repository.)

## Production stores

| Role | Manifest path | Rows | MD5 |
|---|---|---:|---|
| Active tennis SSoT | `tennis/master_store_tennis_SSoT.json` | 17,286 | `fa273ca4d54563866e370a7178edc4fc` |
| Football verification target | `football/master_store_15767.json` | 15,767 | `bf2dd9b40e1dda6a4546394107f44a5a` |

The tennis directory contains exactly one production store. Its current approval card is
`tennis/APPROVAL-CARD-TENNIS-GS134-2026-08-17.md` (T-003 remediation 2026-08-18 appended to its transaction chain). Read each sport's
`KNOWN-GAPS.md` before using its data. A matching hash proves that bytes are unchanged; it
does not prove that the dataset is complete.

## Verification

Run from the repository root:

```bash
python3 Engineering/tools/verify_data.py
python3 Engineering/tools/verify_data.py --json
```

Without `--store`, the verifier discovers the repository root, opens
`data/MANIFEST.json`, and resolves `active_store.path` relative to that
manifest. `--manifest` and `--store` remain available for explicit forensic checks.

Exit status `0` means every implemented claim was reproduced from disk. Exit status `1`
means at least one check failed.

## Admission rules

1. Do not place staging artifacts, engineering code, CSV outputs, or alternate stores in the production tree.
2. Keep executable tools and generated leaderboards under `Engineering/`.
3. Do not hardcode an active-store filename; read it from `MANIFEST.json`.
4. Update manifest row counts and digests whenever an approved store changes.
5. Keep gaps explicit and reproducible.
6. No quarantined artifact enters the SSoT without forensic approval.
