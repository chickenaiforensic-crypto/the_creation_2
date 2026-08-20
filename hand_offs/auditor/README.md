# Auditor hand-offs

Independent audit artifacts for `the_creation_2`. Auditors recompute from bytes. A report is not itself evidence.

| Date | Auditor | Artifact | Verdict (short) |
|---|---|---|---|
| 2026-08-20 | Auditor 5 | [AUDITOR-5-ORIENT-AND-INDEPENDENT-RECOMPUTE-2026-08-20.md](AUDITOR-5-ORIENT-AND-INDEPENDENT-RECOMPUTE-2026-08-20.md) | Stores authentic against MANIFEST pins. `data/README.md` rejected (stale tennis pin). Dedura join-key drift and 82 empty-sourceId MOL Cup rows are new defects. |

Reproduce Auditor 5:

```bash
python3 hand_offs/auditor/recompute.py
```
