import os
import io
from flask import Flask, request, send_file
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route('/')
def home():
    return "Servidor Ativo! Use /browse?url=https://www.google.com"

@app.route('/browse')
def browse():
    url = request.args.get('url', 'https://www.google.com')
    x = request.args.get('x')
    y = request.args.get('y')

    try:
        with sync_playwright() as p:
            # Lança o Chrome com o modo seguro para servidores
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            page = browser.new_page(viewport={'width': 1280, 'height': 720})
            page.goto(url, wait_until="load", timeout=30000)

            if x and y:
                page.mouse.click(float(x), float(y))
                page.wait_for_timeout(2000)

            screenshot = page.screenshot()
            browser.close()
            return send_file(io.BytesIO(screenshot), mimetype='image/png')
    except Exception as e:
        return f"Erro no navegador: {str(e)}", 500

if __name__ == '__main__':
    # O Render usa a porta 10000 por padrão para Docker
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
