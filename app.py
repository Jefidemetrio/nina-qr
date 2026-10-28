from flask import Flask
import os
import urllib.request
import json
app = Flask(__name__)

BRIDGE_URL = os.getenv('BRIDGE_URL', 'http://127.0.0.1:3001/qr')

@app.route('/')
def index():
    try:
        with urllib.request.urlopen(BRIDGE_URL, timeout=5) as resp:
            data = json.load(resp)
        status = data.get('status', 'unknown')
        has_qr = data.get('hasQr', False)
        qr_ascii = data.get('qrAscii', '')
        if has_qr and qr_ascii:
            html = f'''<html><body>
<h3>QR Code de conexão WhatsApp - Nina</h3>
<pre style="white-space:pre-wrap;word-break:break-all;font-family:monospace;background:#f5f5f5;padding:10px;">{qr_ascii}</pre>
<hr>
<p>Status: {status}</p>
</body></html>'''
            return html
        else:
            return f'<html><body><pre>Status: {status}<br>QR ainda não disponível. Aguarde o bridge gerar.</pre></body></html>'
    except Exception as e:
        return f'<html><body><pre>Erro ao buscar QR do bridge: {e}</pre></body></html>'

app.run(host='0.0.0.0', port=8000)
