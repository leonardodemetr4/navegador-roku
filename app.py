import os
import io
from flask import Flask, request, send_file, redirect
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route('/')
def home():
    # Se entrar no link puro, ele pula direto para o Google
    return redirect("/browse?url=https://www.google.com")

@app.route('/browse')
def browse():
    # Pega a URL. Se não vier nada, usa o Google.
    url = request.args.get('url')
    if not url or url.strip() == "":
        url = "https://www.google.com"
        
    x = request.args.get('x')
    y = request.args.get('y')

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            page = browser.new_page(viewport={'width': 1280, 'height': 720})
            
            # Garante que o link seja válido
            if not url.startswith("http"):
                url = "https://" + url

            page.goto(url, wait_until="load", timeout=30000)

            if x and y and x != "None" and y != "None":
                page.mouse.click(float(x), float(y))
                page.wait_for_timeout(2000)

            screenshot = page.screenshot()
            browser.close()
            return send_file(io.BytesIO(screenshot), mimetype='image/png')
    except Exception as e:
        return f"Erro: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
