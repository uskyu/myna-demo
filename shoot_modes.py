import os
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8090"
OUT = "/root/myna-demo-pages/screenshots"

modes = ["guided", "manual", "free", "strict"]

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 900, "height": 900}, device_scale_factor=2)
    for mode in modes:
        pg = ctx.new_page()
        pg.goto(f"{BASE}/02-handoff-rules.html", wait_until="networkidle")
        pg.wait_for_timeout(400)
        # 通过 select 切换模式
        pg.select_option("#modeSelect", mode)
        pg.wait_for_timeout(700)
        # 只截协作模式那一块（第一个 section）
        el = pg.query_selector(".settings-panel .section")
        el.screenshot(path=f"{OUT}/mode-{mode}.png")
        print("OK mode", mode)
        pg.close()
    ctx.close()
    browser.close()
print("DONE")
