from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "screenshots"
OUT.mkdir(exist_ok=True)
URL = "http://127.0.0.1:8091/"

with sync_playwright() as p:
    browser = p.chromium.launch()
    configs = [
        ("desktop-onepage", {"width": 1440, "height": 960}, 2, False),
        ("mobile-onepage", {"width": 390, "height": 844}, 3, True),
    ]
    for name, viewport, dsf, is_mobile in configs:
        ctx = browser.new_context(viewport=viewport, device_scale_factor=dsf, is_mobile=is_mobile)
        page = ctx.new_page()
        errors = []
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(8200)
        metrics = page.evaluate("""() => ({
            scrollWidth: document.documentElement.scrollWidth,
            clientWidth: document.documentElement.clientWidth,
            activeRows: document.querySelectorAll('.chat-row.active').length,
            doneTools: document.querySelectorAll('.tool-card.done').length,
            title: document.title
        })""")
        page.screenshot(path=str(OUT / f"{name}.png"), full_page=True)
        print(name, metrics, "console_errors", errors)
        ctx.close()
    browser.close()
