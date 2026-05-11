#!/usr/bin/env bash
# Finpath Newsroom — local setup script
# Chạy 1 lần sau khi pull repo về:  bash setup.sh

set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

echo ""
echo "================================================"
echo "  Finpath Newsroom — Local Setup"
echo "================================================"
echo ""

# ---------- 1. Python env ----------
echo "[1/5] Python virtualenv + dependencies..."
if ! command -v uv >/dev/null 2>&1; then
  echo "  → uv chưa có. Cài uv trước: https://docs.astral.sh/uv/getting-started/installation/"
  echo "    Mac/Linux:  curl -LsSf https://astral.sh/uv/install.sh | sh"
  exit 1
fi
uv venv --quiet
uv sync --quiet
echo "  ✓ .venv ready"

# ---------- 2. SQLite DB ----------
echo ""
echo "[2/5] SQLite DB (data/pipeline.db)..."
if [ -f "data/pipeline.db" ]; then
  echo "  ✓ data/pipeline.db đã tồn tại — skip"
else
  sqlite3 data/pipeline.db < data/pipeline.schema.sql
  echo "  ✓ tạo data/pipeline.db từ schema"
fi

# ---------- 3. Secrets file ----------
echo ""
echo "[3/5] Secrets file (data/secrets.yaml)..."
if [ -f "data/secrets.yaml" ]; then
  echo "  ✓ data/secrets.yaml đã tồn tại — skip"
else
  cp data/secrets.yaml.example data/secrets.yaml
  echo "  ✓ copy template từ .example — cần fill key (xem cuối script)"
fi

# ---------- 4. Web (npm install) ----------
echo ""
echo "[4/5] Web viewer (web/node_modules)..."
if ! command -v npm >/dev/null 2>&1; then
  echo "  ✗ npm chưa có. Cài Node.js >= 18: https://nodejs.org/"
  exit 1
fi
if [ -d "web/node_modules" ]; then
  echo "  ✓ web/node_modules đã có — skip (chạy lại 'cd web && npm install' nếu cần update)"
else
  (cd web && npm install --silent)
  echo "  ✓ web deps installed"
fi

# ---------- 5. Worker (optional) ----------
echo ""
echo "[5/5] Cloudflare Worker (worker/node_modules) — optional cho comment box..."
if [ -d "worker/node_modules" ]; then
  echo "  ✓ worker/node_modules đã có — skip"
else
  (cd worker && npm install --silent)
  echo "  ✓ worker deps installed"
fi

# ---------- Final message ----------
echo ""
echo "================================================"
echo "  Setup xong. Cần xin sếp những key sau:"
echo "================================================"
echo ""
echo "Sếp ơi đưa em mấy cái key này để fill vào data/secrets.yaml:"
echo ""
echo "  1. telegram.bot_token              — token Telegram bot (@BotFather)"
echo "  2. telegram.chat_id                — Telegram channel chat_id (-100...)"
echo "  3. telegram.linked_group_chat_id   — Telegram group thảo luận linked với channel (-100...)"
echo "  4. telegram.feedback_group_chat_id — Telegram group nhận comment feedback (-100...)"
echo "  5. telegram.base_url               — URL public của web (vd https://...github.io/finpath-newsroom)"
echo "  6. github.token                    — GitHub PAT scope 'repo' để poll Pages deploy"
echo ""
echo "Optional (chỉ cần nếu deploy Cloudflare Worker cho comment box):"
echo "  7. Cloudflare account login (wrangler login)"
echo "  8. KV namespace id (sau khi chạy: wrangler kv:namespace create FEEDBACK_RL)"
echo "  9. Worker URL (sau khi deploy) — set vào VITE_FEEDBACK_WORKER_URL lúc build web"
echo ""
echo "Sau khi sếp đưa key:"
echo "  → mở data/secrets.yaml, dán key vào các field tương ứng"
echo "  → test: source .venv/bin/activate && pytest"
echo "  → chạy web: cd web && npm run dev  (http://localhost:5174)"
echo ""
