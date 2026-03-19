from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
        "./user-data",
        headless=False,
        slow_mo=500,
        permissions=["clipboard-read", "clipboard-write"],
        chromium_sandbox=False,
    )
        page = browser.new_page()
        page.goto("https://the-internet.herokuapp.com/login")
        locartor_name = page.locator("#username").fill('tomsmith')
        locartor_password = page.locator("#password").fill('SuperSecretPassword!')
        locator_botao = page.locator("button[type=submit]").click()
        time.sleep(5)
        locator_text_secure = page.locator(".subheader")
        if(locator_text_secure.inner_text() == "Welcome to the Secure Area. When you are done click logout below."):
                page.screenshot(path='playwright_exe1.png')
                print(locator_text_secure.inner_html())

        page.goto("https://the-internet.herokuapp.com/checkboxes")
        checkboxes = page.locator('input[type="checkbox"]')
        print(f'Total de checkboxes: {checkboxes.count()}')
        estado1 = checkboxes.nth(0).is_checked()
        estado2 = checkboxes.nth(1).is_checked()
        print(f'\nEstado inicial:')
        print(f'  Checkbox 1: {"marcado" if estado1 else "desmarcado"}')
        print(f'  Checkbox 2: {"marcado" if estado2 else "desmarcado"}')
        checkboxes.nth(0).check()
        print(f'\nApós check() no checkbox 1: {checkboxes.nth(0).is_checked()}')
        checkboxes.nth(1).uncheck()
        print(f'Após uncheck() no checkbox 2: {checkboxes.nth(1).is_checked()}')
        print(f'\nInvertendo estados:')
        for i in range(checkboxes.count()):
            checkbox = checkboxes.nth(i)
            if checkbox.is_checked():
                checkbox.uncheck()
            else:
                checkbox.check()
        print(f'  Checkbox {i+1}: {"marcado" if checkbox.is_checked() else "desmarcado"}')
        time.sleep(3)
        page.screenshot(path='playwright_exe2.png')


