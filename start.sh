#!/bin/bash
set -e

# подгружаем .env если есть
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs || true)
fi

echo "BOT_TOKEN задан? ${BOT_TOKEN:+yes}"

# поднимаем минимальный HTTP healthcheck на нужном порту в фоне
python - <<'PYTHON' &
import os, http.server, socketserver, json
port = int(os.getenv("PORT", "8000"))
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status":"ok"}).encode())
    def log_message(self, fmt, *args):
        pass  # чтобы не шумел
with socketserver.TCPServer(("", port), H) as srv:
    srv.serve_forever()
PYTHON

exec python bot.py
