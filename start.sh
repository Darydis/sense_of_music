#!/usr/bin/env bash
set -euo pipefail

: "${PORT:?PORT must be set by platform}"  # без $PORT сразу падаем (удобно диагностировать)
echo "BOT_TOKEN задан? ${BOT_TOKEN:+yes}"

echo "PORT=${PORT:-8000}"
: "${PORT:=8000}"   # если платформа не проставит, используем 8000

# лёгкий health-server, чтобы платформа видела открытый порт
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

# запускаем polling-бота (замени имя файла, если другое)
exec python bot.py
