import os
import io
from flask import Flask, request, send_file
from playwright.sync_api import sync_playwright

app = Flask(__name__)

# Função que tira o print
def capturar_tela(url, x=None, y=None):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            page = browser.new_page(viewport={'width': 1280, 'height': 720})
            
            # Se a URL não começar com http, ele coloca
            if not url.startswith("http"):
                url = "https://" + url
                
            page.goto(url, wait_until="load", timeout=30000)

            # Se houver clique
            if x and y and x != "None":
                page.mouse.click(float(x), float(y))
                page.wait_for_timeout(2000)

            img = page.screenshot()
            browser.close()
            return img
    except Exception as e:
        print(f"Erro: {e}")
        return None

# Rota principal (Agora ela manda a foto do Google direto!)
@app.route('/')
def home():
    img_data = capturar_tela("https://www.google.com")
    return send_file(io.BytesIO(img_data), mimetype='image/png')

# Rota de navegação
@app.route('/browse')
def browse():
    url = request.args.get('url', 'https://www.google.com')
    x = request.args.get('x')
    y = request.args.get('y')
    img_data = capturar_tela(url, x, y)
    if img_data:
        return send_file(io.BytesIO(img_data), mimetype='image/png')
    return "Erro", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
