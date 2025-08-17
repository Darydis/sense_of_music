#!/usr/bin/env bash
set -euo pipefail
set -x

# порт от платформы, по умолчанию 8000 (на всякий)
PORT=${PORT:-8000}
export PORT
echo "BOT_TOKEN set? ${BOT_TOKEN:+yes}"

python - <<'PY'
import os, socket, urllib.parse
u = urllib.parse.urlparse(os.getenv("proxy_url",""))
host, port = u.hostname, u.port
print("Proxy target:", host, port)
try:
    s=socket.create_connection((host,port), timeout=5)
    print("Proxy TCP: OK")
    s.close()
except Exception as e:
    print("Proxy TCP: FAIL ->", e)
PY

python - <<'PY'
import os, httpx
px = os.getenv("proxy_url")
try:
    r = httpx.get(
      "https://api.openai.com/v1/models",
      headers={"Authorization":"Bearer INVALID"},  # спецом
      proxies={"http": px, "https": px},
      timeout=httpx.Timeout(10, connect=10, read=10, write=10, pool=10),
      trust_env=False,
    )
    print("OpenAI via proxy ->", r.status_code, r.text[:80])
except Exception as e:
    print("OpenAI via proxy FAIL ->", type(e).__name__, e)
PY


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
