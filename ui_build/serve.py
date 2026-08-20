"""
serve.py — minimal static server for the blank UI rebuild. Version: v1.3

Serves ui_build/app/ on 0.0.0.0:8080 (preview-friendly, no caching).
No backend API: the UI reads the prebuilt, checksum-verified index.json.

Usage: python3 ui_build/serve.py
"""
import http.server
import os

PORT = int(os.environ.get("PORT", "8080"))
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


if __name__ == "__main__":
    print(f"Serving {ROOT} on 0.0.0.0:{PORT}")
    http.server.ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
