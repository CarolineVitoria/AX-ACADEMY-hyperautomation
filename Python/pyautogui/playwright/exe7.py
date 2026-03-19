# Comparar todas as formas de localizar o mesmo elemento
# Importa a API síncrona do Playwright
from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False, slow_mo=600)
    page = browser.new_page()
    page.goto('https://www.saucedemo.com')
    page.wait_for_load_state('networkidle')

    print('Testando diferentes formas de localizar o campo Username:\n')

    # ── Forma 1: get_by_placeholder ────────────────────────────────────
    # Localiza pelo texto do placeholder do input
    locator1 = page.get_by_placeholder('Username')
    locator1.fill('standard_user')
    print('1. get_by_placeholder: OK')
    locator1.clear()

    # ── Forma 2: get_by_test_id (requer configuração) ──────────────────
    # Configura o Playwright para usar data-test como atributo de teste
    p.selectors.set_test_id_attribute('data-test')
    locator2 = page.get_by_test_id('username')
    locator2.fill('standard_user')
    print('2. get_by_test_id: OK')
    locator2.clear()

    # ── Forma 3: CSS por id ────────────────────────────────────────────
    # O # indica seleção por id no CSS
    locator3 = page.locator('#user-name')
    locator3.fill('standard_user')
    print('3. CSS por id: OK')
    locator3.clear()

    # ── Forma 4: CSS por atributo data-test ────────────────────────────
    # Seletor CSS que busca pelo atributo data-test
    locator4 = page.locator('[data-test="username"]')
    locator4.fill('standard_user')
    print('4. CSS por atributo data-test: OK')
    locator4.clear()

    # ── Forma 5: CSS por name ──────────────────────────────────────────
    # Seletor CSS que busca pelo atributo name
    locator5 = page.locator('[name="user-name"]')
    locator5.fill('standard_user')
    print('5. CSS por name: OK')
    locator5.clear()

    # ── Forma 6: XPath ─────────────────────────────────────────────────
    # XPath que busca input com id igual a user-name
    locator6 = page.locator("//input[@id='user-name']")
    locator6.fill('standard_user')
    print('6. XPath: OK')
    locator6.clear()

    print('\nTodas as formas funcionaram!')
    browser.close()
