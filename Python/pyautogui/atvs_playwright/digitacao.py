from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        "./user-data",
        headless=False,
        slow_mo=500,
        permissions=["clipboard-read", "clipboard-write"]
    )

    page = browser.new_page()
    page.goto('https://the-internet.herokuapp.com/inputs')
    page.wait_for_load_state('networkidle')

    locator_input = page.locator("input[type=number]")
    locator_input.type("1000", delay=100)
    locator_input.page.keyboard.press('Backspace')
    locator_input.page.keyboard.press('Backspace')
    locator_input.type("5", delay=100)
    #page.keyboard.press('Control+C')
    locator_input.page.keyboard.press('Control+A')
    locator_input.type("9999", delay=100)
    conteudo = locator_input.input_value()
    print(conteudo)

    page2 = browser.new_page()
    page2.goto('https://www.rapidtables.com/tools/notepad.html')
    page2.wait_for_load_state('networkidle')


    locator_text = page2.locator("#bar")
    locator_text.type("Playwright automatiza browsers com precisao. RPA com Python e muito poderoso. Aprenda automacao na pratica")
    locator_text.page.keyboard.press('Control+A')
    locator_text.page.keyboard.press('Control+C')
    locator_text.page.keyboard.press('Enter')
    locator_text.page.keyboard.press('Enter')
    locator_text.focus()
   
    locator_bt_colar = page2.locator('button.btn:nth-child(6)').click()
    #locator_text.page.keyboard.press('Control+V')
    time.sleep(2)
    page2.screenshot(path='Atv_texto.png')
    print('Screenshot da atv salvo')
    browser.close()