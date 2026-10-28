from flask import Flask
from pathlib import Path
app = Flask(__name__)
LOG = Path('/data/bridge_stdout.log')

@app.route('/')
def index():
    try:
        if not LOG.exists():
            msg = 'Arquivo de log ainda não existe em /data/bridge_stdout.log. Aguarde o bridge gerar o arquivo.'
            return f'<html><body><pre>{msg}</pre></body></html>'
        if LOG.is_dir():
            candidates = list(LOG.glob('bridge_stdout.log*'))
            if not candidates:
                msg = 'Caminho /data/bridge_stdout.log é um diretório vazio.'
                return f'<html><body><pre>{msg}</pre></body></html>'
            log_file = candidates[0]
        else:
            log_file = LOG
        text = log_file.read_text(errors='ignore')
        marker = 'Scan this QR code with WhatsApp on your phone:'
        start = text.find(marker)
        if start != -1:
            start += len(marker)
            end = text.find('Waiting for scan', start)
            if end != -1:
                qr_block = text[start:end].strip()
                qr_block = '\n'.join([l for l in qr_block.splitlines() if l.strip()])
                if qr_block:
                    return f'<html><body><h3>QR Code de conexão</h3><pre style="white-space:pre-wrap;word-break:break-all;">{qr_block}</pre><hr><p>Últimas linhas do log:</p><pre>{text[-1000:]}</pre></body></html>'
        last = text[-2000:]
        msg = 'QR não encontrado no padrão esperado. Exibindo últimas 2000 caracteres do log:\n\n' + last
        return f'<html><body><pre>{msg}</pre></body></html>'
    except Exception as e:
        return f'<html><body><pre>Erro: {e}</pre></body></html>'

app.run(host='0.0.0.0', port=8000)
