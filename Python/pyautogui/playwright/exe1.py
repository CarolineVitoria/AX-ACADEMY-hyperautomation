# Importa a API síncrona do Playwright
from importlib.metadata import version
from playwright.sync_api import sync_playwright

# Versão da biblioteca Playwright
print(f'Playwright: {version("playwright")}')

# Inicia o Playwright — o 'with' garante liberação dos recursos ao final
with sync_playwright() as p:

    # Abre o Chromium sem interface gráfica
    browser = p.chromium.launch(headless=False)
    print(f'Versão do Chromium: {browser.version}')

    # Abre uma nova página
    page = browser.new_page()

    # Navega para o site de testes
    page.goto('https://www.saucedemo.com')

    # Captura o título da aba do browser
    # title() retorna o texto do elemento <title> da página
    titulo = page.title()

    # Imprime o título capturado
    print(f'Título da página: {titulo}')

    # Captura a URL atual da página
    url = page.url

    # Imprime a URL
    print(f'URL atual: {url}')

    # Tira screenshot como prova que funcionou
    page.screenshot(path='verificacao.png')
    print('Screenshot salvo: verificacao.png')

    # Fecha o browser
    browser.close()