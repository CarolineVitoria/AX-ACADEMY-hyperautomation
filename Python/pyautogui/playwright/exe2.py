# Testar os três browsers na mesma execução
# Gera três screenshots

# Importa a API síncrona do Playwright
from playwright.sync_api import sync_playwright

# Inicia o Playwright
with sync_playwright() as p:

    # Cria uma lista com os três browsers disponíveis
    # Cada item é um objeto de tipo BrowserType
    browsers_disponiveis = [
        p.chromium,   # Google Chrome / Edge
        p.firefox,    # Mozilla Firefox
        p.webkit,     # Webkit
    ]

    # Percorre cada browser da lista
    for browser_type in browsers_disponiveis:

        # Imprime qual browser está sendo testado
        # browser_type.name retorna 'chromium', 'firefox' ou 'webkit'
        print(f'\nTestando: {browser_type.name}')

        # Abre o browser atual sem interface gráfica
        browser = browser_type.launch(headless=True)

        # Abre uma nova página
        page = browser.new_page()

        # Navega para o site de testes
        page.goto('https://www.saucedemo.com', wait_until='networkidle')

        # Captura o título da página
        titulo = page.title()

        # Imprime o resultado
        print(f'  Título: {titulo}')
        print(f'  URL: {page.url}')

        # Define o nome do arquivo usando o nome do browser
        nome_arquivo = f'screenshot_{browser_type.name}.png'

        # Tira screenshot com nome específico de cada browser
        page.screenshot(path=nome_arquivo)
        print(f'  Screenshot salvo: {nome_arquivo}')

        # Fecha o browser antes de abrir o próximo
        browser.close()

    print('\nTodos os browsers testados com sucesso!')
