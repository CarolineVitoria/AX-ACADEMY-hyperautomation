# Sync: acessar três páginas em sequência

# Importa a API síncrona do Playwright
from playwright.sync_api import sync_playwright

# Importa datetime para medir o tempo total
from datetime import datetime

# Registra o tempo de início
inicio = datetime.now()

# Lista de URLs para acessar em sequência
urls = [
    'https://www.saucedemo.com',
    'https://www.selenium.dev/selenium/web/web-form.html',
    'https://the-internet.herokuapp.com',
]

with sync_playwright() as p:

    # Abre o browser
    browser = p.chromium.launch(headless=True)

    # Abre uma página — será reutilizada para cada URL
    page = browser.new_page()

    # Percorre cada URL da lista
    for url in urls:

        # Navega para a URL atual
        # No modo sync, o script PARA aqui até a página carregar
        page.goto(url)

        # Aguarda a rede ficar quieta
        page.wait_for_load_state('networkidle')

        # Captura o título da página
        titulo = page.title()

        # Imprime o resultado
        print(f'URL: {url}')
        print(f'Título: {titulo}')
        print()

    # Fecha o browser
    browser.close()

# Calcula o tempo total
total = (datetime.now() - inicio).total_seconds()
print(f'Tempo total (sequencial): {total:.2f} segundos')
