#!/usr/bin/env bash
set -euo pipefail
set -x

# порт от платформы, по умолчанию 8000 (на всякий)
PORT=${PORT:-8000}
export PORT
echo "BOT_TOKEN set? ${BOT_TOKEN:+yes}"

# лёгкий health сервер, чтобы платформа видела открытый порт
python - <<'PY' &
import os, http.server, socketserver, json
port = int(os.getenv("PORT", "8000"))
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.send_header("Content-Type","application/json")
        self.end_headers(); self.wfile.write(json.dumps({"status":"ok"}).encode())
    def log_message(self, *a): pass
with socketserver.TCPServer(("", port), H) as srv: srv.serve_forever()
PY

# запускаем бота в ФОРЕГРАУНДЕ и без буферизации (лог трейсбеков в stdout)
python -u bot.py || { echo "bot crashed with code $?"; sleep 600; exit 1; }
