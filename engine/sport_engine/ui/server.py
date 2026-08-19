"""SaaS UI dev server — serves the zero-hardcoded frontend + JSON API.

Endpoints:
  GET /                    -> index.html
  GET /app.js              -> app.js
  GET /styles.css          -> styles.css
  GET /api/ui              -> ui_manifest()
  GET /api/options         -> player_options()
  GET /api/matchup?a=..&b=..&tournaments=..&years=..&tours=..&from=.. -> matchup_report()

All labels/options come from config via the api module — no frontend-side
hardcoding; app.js reads the manifest from /api/ui and renders from it.
"""

from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ENGINE_ROOT = Path(__file__).resolve().parents[2]  # engine/
sys.path.insert(0, str(ENGINE_ROOT))

from sport_engine.ui.api import matchup_report, performance_report, player_options, ui_manifest  # noqa: E402

FRONTEND = Path(__file__).resolve().parent / "frontend"


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, data) -> None:
        self._send(200, json.dumps(data).encode("utf-8"), "application/json")

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path == "/":
            path = "/index.html"
        if path.startswith("/api/"):
            if path == "/api/ui":
                self._json(ui_manifest())
            elif path == "/api/options":
                self._json(player_options())
            elif path == "/api/matchup":
                q = parse_qs(parsed.query)
                a = (q.get("a") or [""])[0]
                b = (q.get("b") or [""])[0]
                if not a or not b:
                    self._send(400, b'{"error":"a and b are required"}', "application/json")
                    return
                tours = q.get("tours", []) or []
                tournaments = q.get("tournaments", []) or []
                years = q.get("years", []) or []
                from_date = (q.get("from") or [None])[0]
                try:
                    self._json(
                        matchup_report(
                            player_a=a,
                            player_b=b,
                            tournaments=tournaments,
                            years=years,
                            tours=tours,
                            from_date=from_date,
                        )
                    )
                except Exception as exc:  # surface engine errors to the UI
                    self._send(500, json.dumps({"error": str(exc)}).encode(), "application/json")
            elif path == "/api/performance":
                q = parse_qs(parsed.query)
                a = (q.get("a") or [""])[0]
                b = (q.get("b") or [""])[0]
                if not a or not b:
                    self._send(400, b'{"error":"a and b are required"}', "application/json")
                    return
                tours = q.get("tours", []) or []
                tournaments = q.get("tournaments", []) or []
                years = q.get("years", []) or []
                try:
                    self._json(
                        performance_report(
                            player_a=a,
                            player_b=b,
                            tournaments=tournaments,
                            years=years,
                            tours=tours,
                        )
                    )
                except Exception as exc:  # surface engine errors to the UI
                    self._send(500, json.dumps({"error": str(exc)}).encode(), "application/json")
            else:
                self._send(404, b"not found", "application/json")
            return
        file = FRONTEND / path.lstrip("/")
        if not file.is_file() or file.suffix not in (".html", ".js", ".css"):
            self._send(404, b"not found", "text/plain")
            return
        ctype = {".html": "text/html", ".js": "application/javascript", ".css": "text/css"}[file.suffix]
        self._send(200, file.read_bytes(), ctype)

    def log_message(self, fmt, *args):
        sys.stderr.write(f"[ui] {fmt % args}\n")


def main(port: int = 8080) -> None:
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"UI server on http://0.0.0.0:{port}")
    server.serve_forever()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    main(port)
