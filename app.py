from flask import Flask
from pathlib import Path
import os
app = Flask(__name__)
# Bridge do WhatsApp da Nina escreve em /tmp/bridge_stdout.log
LOG = Path(os.getenv('BRIDGE_LOG', '/tmp/bridge_stdout.log'))

@app.route('/')
def index():
    try:
        # Garante que o caminho existe e é um arquivo
        if LOG.exists() and LOG.is_dir():
            # Se é diretório, tenta usar arquivo dentro ou criar um
            candidates = list(LOG.glob('bridge_stdout.log*'))
            if candidates:
                log_file = candidates[0]
            else:
                # Diretório vazio: cria arquivo de exemplo com QR de demonstração
                log_file = LOG / 'bridge_stdout.log'
                sample = 'Scan this QR code with WhatsApp on your phone:\n\n' + \
                         '████████████████████████████████\n' + \
                         '████████████████████████████████\n' + \
                         '█   QR DE CONEXÃO NÃO GERADO    █\n' + \
                         '█   Bridge não iniciado ainda   █\n' + \
                         '████████████████████████████████\n' + \
                         '████████████████████████████████\n' + \
                         '\nWaiting for scan\n'
                log_file.write_text(sample, encoding='utf-8')
        elif not LOG.exists():
            # Cria arquivo se não existe
            LOG.parent.mkdir(parents=True, exist_ok=True)
            sample = 'Scan this QR code with WhatsApp on your phone:\n\n' + \
                     '████████████████████████████████\n' + \
                     '█   QR DE CONEXÃO NÃO GERADO    █\n' + \
                     '█   Bridge não iniciado ainda   █\n' + \
                     '████████████████████████████████\n' + \
                     '\nWaiting for scan\n'
            LOG.write_text(sample, encoding='utf-8')
            log_file = LOG
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
                    html = f'''<html><body>
<h3>QR Code de conexão</h3>
<pre style="white-space:pre-wrap;word-break:break-all;font-family:monospace;">{qr_block}</pre>
<hr>
<p>Log está sendo monitorado em: {log_file}</p>
<pre>{text[-1000:]}</pre>
</body></html>'''
                    return html
        # Fallback: mostra log bruto
        last = text[-2000:]
        msg = 'QR não encontrado no padrão esperado. Exibindo log:\n\n' + last
        return f'<html><body><pre>{msg}</pre></body></html>'
    except Exception as e:
        return f'<html><body><pre>Erro: {e}</pre></body></html>'

app.run(host='0.0.0.0', port=8000)
