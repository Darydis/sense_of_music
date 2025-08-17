#!/bin/bash
set -xeuo pipefail

# показать, что видит платформа
echo "PORT=${PORT:-unset}"
echo "BOT_TOKEN задан? ${BOT_TOKEN:+yes}"

# если $PORT не задан — лучше фейлить, чтобы сразу понять причину
: "${PORT:?PORT must be set by platform}"

# health-сервер в фоне (как у тебя)
python - <<'PY' &
import os, http.server, socketserver, json
port = int(os.getenv("PORT"))
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.send_header("Content-Type","application/json")
        self.end_headers(); self.wfile.write(json.dumps({"status":"ok"}).encode())
    def log_message(self, *a): pass
with socketserver.TCPServer(("", port), H) as srv: srv.serve_forever()
PY

# сам бот
exec python bot.py
