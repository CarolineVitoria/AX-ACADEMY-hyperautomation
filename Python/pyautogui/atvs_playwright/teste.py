from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=1000)
    
    page2 = browser.new_page()
    page2.goto('https://pt.anotepad.com/')
    page2.wait_for_load_state('networkidle')

    locator_text = page2.locator(".form-control textarea ")
    locator_text.type("Playwright automatiza browsers com precisao. RPA com Python e muito poderoso. Aprenda automacao na pratica", delay=80)
    browser.close()