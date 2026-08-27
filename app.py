import os
from flask import Flask, request, send_file
from playwright.sync_api import sync_playwright
import io

app = Flask(__name__)

# Rota principal para não dar erro ao abrir o link puro
@app.route('/')
def index():
    return "Servidor do Navegador Roku está Ativo! Use a rota /browse"

def get_screenshot(url, x=None, y=None):
    with sync_playwright() as p:
        # Adicionamos argumentos de segurança para o Render
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()
        
        try:
            # Tenta carregar o site, se demorar mais de 20 segundos ele para
            page.goto(url, wait_until="load", timeout=20000)
            
            # Se recebeu coordenadas de clique, ele clica
            if x and y and x != "None" and y != "None":
                try:
                    page.mouse.click(float(x), float(y))
                    page.wait_for_timeout(1000) # Espera 1 segundo após clicar
                except:
                    print("Erro ao clicar")

            img = page.screenshot()
            browser.close()
            return img
        except Exception as e:
            print(f"Erro na navegação: {e}")
            browser.close()
            return None

@app.route('/browse')
def browse():
    url = request.args.get('url', 'https://www.google.com')
    x = request.args.get('x')
    y = request.args.get('y')
    
    img_data = get_screenshot(url, x, y)
    
    if img_data:
        return send_file(io.BytesIO(img_data), mimetype='image/png')
    else:
        return "Erro ao capturar imagem do site", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
