import os
from flask import Flask, request, send_file
from playwright.sync_api import sync_playwright
import io

app = Flask(__name__)

def get_screenshot(url, x=None, y=None):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1280, 'height': 720})
        page.goto(url, wait_until="networkidle")
        if x and y:
            page.mouse.click(float(x), float(y))
            page.wait_for_timeout(2000)
        img = page.screenshot()
        browser.close()
        return img

@app.route('/browse')
def browse():
    url = request.args.get('url', 'https://www.google.com')
    x = request.args.get('x')
    y = request.args.get('y')
    img_data = get_screenshot(url, x, y)
    return send_file(io.BytesIO(img_data), mimetype='image/png')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
