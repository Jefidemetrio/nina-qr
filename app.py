from flask import Flask
import re
from pathlib import Path
app = Flask(__name__)
LOG = Path('/data/bridge_stdout.log')
@app.route('/')
def index():
    try:
        if not LOG.exists():
            qr = 'Arquivo de log ainda não existe em /data/bridge_stdout.log. Aguarde o bridge gerar o arquivo.'
        elif LOG.is_dir():
            candidates = list(LOG.glob('bridge_stdout.log*'))
            if candidates:
                log_file = candidates[0]
            else:
                qr = 'Caminho /data/bridge_stdout.log é um diretório e não contém arquivo de log.'
                return f'<html><body><pre>{qr}</pre></body></html>'
        else:
            log_file = LOG
        text = log_file.read_text(errors='ignore')
        # Extrai o conteúdo entre o marcador e Waiting for scan
        m = re.search(r'Scan this QR code with WhatsApp on your phone:\n+(.*?)\\nWaiting for scan', text, re.S)
        qr = m.group(1).strip() if m else 'QR não encontrado ainda. Aguarde o bridge gerar.'
    except Exception as e:
        qr = f'Erro: {e}'
    return f'<html><body><pre>{qr}</pre></body></html>'
app.run(host='0.0.0.0', port=8000)
