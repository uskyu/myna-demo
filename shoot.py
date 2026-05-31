import os
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8090"
OUT = "/root/myna-demo-pages/screenshots"
os.makedirs(OUT, exist_ok=True)

# (path, name, wait_ms) — 03 是动态播放，等动画播完
pages = [
    ("index.html", "00-home", 1200),
    ("01-chain-collaboration.html", "01-chain", 1200),
    ("02-handoff-rules.html", "02-handoff", 1200),
    ("03-streaming-tools.html", "03-streaming", 13000),
]

with sync_playwright() as p:
    browser = p.chromium.launch()

    # Desktop 1440
    ctx_d = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
    for path, name, wait in pages:
        pg = ctx_d.new_page()
        pg.goto(f"{BASE}/{path}", wait_until="networkidle")
        pg.wait_for_timeout(wait)
        pg.screenshot(path=f"{OUT}/desktop-{name}.png", full_page=True)
        print("OK desktop", name)
        pg.close()
    ctx_d.close()

    # Mobile 390
    ctx_m = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=3, is_mobile=True)
    for path, name, wait in pages:
        pg = ctx_m.new_page()
        pg.goto(f"{BASE}/{path}", wait_until="networkidle")
        pg.wait_for_timeout(wait)
        pg.screenshot(path=f"{OUT}/mobile-{name}.png", full_page=True)
        print("OK mobile", name)
        pg.close()
    ctx_m.close()

    browser.close()
print("ALL DONE")
