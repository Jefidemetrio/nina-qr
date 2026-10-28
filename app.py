from flask import Flask
import re
from pathlib import Path
app = Flask(__name__)
LOG = Path('/data/bridge_stdout.log')
@app.route('/')
def index():
    try:
        text = LOG.read_text(errors='ignore')
        m = re.search(r'Scan this QR code with WhatsApp on your phone:\n+(.*?)\nWaiting for scan', text, re.S)
        qr = m.group(1).strip() if m else 'QR não encontrado ainda. Aguarde o bridge gerar.'
    except Exception as e:
        qr = f'Erro: {e}'
    return f'<html><body><pre>{qr}</pre></body></html>'
app.run(host='0.0.0.0', port=8000)
