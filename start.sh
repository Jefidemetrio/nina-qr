#!/usr/bin/env bash
set -e

# Diretório do projeto
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# Dependências
python3 -m pip install -q flask

# Sobe o bridge da Nina em background se não estiver rodando
if ! pgrep -f "bridge.js --port 3001" > /dev/null; then
  echo "Iniciando WhatsApp Bridge..."
  nohup node scripts/whatsapp-bridge/bridge.js --port 3001 --session whatsapp-session --mode bot > logs/bridge.log 2>&1 &
  sleep 3
fi

# Sobe o app Flask
export BRIDGE_URL=http://127.0.0.1:3001/qr
echo "Iniciando nina-qr na porta 8000..."
python3 app.py
