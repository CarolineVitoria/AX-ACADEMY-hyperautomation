# Importa a API síncrona do Playwright
from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    # Abre o Chromium com interface gráfica para visualizar a automação
    browser = p.chromium.launch(headless=False)

    # Abre uma nova página
    page = browser.new_page()

    # Navega para o site de testes
    page.goto('https://www.saucedemo.com')

    # Aguarda a página carregar completamente
    page.wait_for_load_state('networkidle')

    # Preenche o campo de usuário pelo placeholder
    page.get_by_placeholder('Username').fill('standard_user')

    # Preenche o campo de senha pelo placeholder
    page.get_by_placeholder('Password').fill('secret_sauce')

    # Clica no botão de login
    page.get_by_role('button', name='Login').click()

    # Aguarda a página de produtos carregar
    page.wait_for_load_state('networkidle')

    # Captura o texto do primeiro produto da lista
    produto = page.locator('[data-test="inventory-item-name"]').first.text_content()

    # Imprime o nome do produto capturado no terminal
    print(f'Primeiro produto encontrado: {produto}')

    # Tira screenshot da página de produtos como evidência
    page.screenshot(path='produtos.png', full_page=True)

    # Imprime confirmação do screenshot
    print('Screenshot salvo em: produtos.png')

    # Fecha o browser e libera os recursos
    browser.close()
