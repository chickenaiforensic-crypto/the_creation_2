"""Data source — loads edition files from the data tree, verifying each file's
SHA-256 and match count against the manifest before use (DATA-RULES Rule 5:
a file and its manifest entry must never drift). Fails loudly on any mismatch —
no silent skip, no fallback.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import List


class DataIntegrityError(RuntimeError):
    """Edition file bytes or count do not match its manifest entry."""


def load_editions(data_root: Path, manifest_file: str, mschema: Mapping) -> List[dict]:
    """Read every edition listed in the manifest, verified. Returns edition data."""
    manifest_path = data_root / manifest_file
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    editions: List[dict] = []
    for entry in manifest[mschema["manifest_editions"]]:
        file_path = data_root / entry[mschema["edition_file_path"]]
        raw = file_path.read_bytes()
        actual = hashlib.sha256(raw).hexdigest()
        expected = entry[mschema["edition_checksum"]]
        if actual != expected:
            raise DataIntegrityError(
                f"checksum mismatch: {entry[mschema['edition_file_path']]} "
                f"(manifest={expected[:12]}..., actual={actual[:12]}...)"
            )
        data = json.loads(raw.decode("utf-8"))
        actual_count = len(data[mschema["edition_file_matches"]])
        expected_count = entry[mschema["edition_match_count"]]
        if actual_count != expected_count:
            raise DataIntegrityError(
                f"count mismatch: {entry[mschema['edition_file_path']]} "
                f"(manifest={expected_count}, actual={actual_count})"
            )
        editions.append(data)
    return editions


def edition_identity(edition: Mapping, mschema: Mapping) -> dict:
    """Manifest-style identity for one loaded edition (tournament, year, count)."""
    return {
        "tournament": edition[mschema["edition_file_tournament"]],
        "year": edition[mschema["edition_file_year"]],
        "match_count": len(edition[mschema["edition_file_matches"]]),
    }
