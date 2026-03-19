# Usar slow_mo

# Importa a API síncrona do Playwright
from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    # slow_mo=800 adiciona 800ms de pausa entre cada ação
    # Ideal para demonstrações em sala de aula —
    # os alunos conseguem acompanhar cada passo visualmente
    browser = p.chromium.launch(
        headless=False,   # abre a janela para visualizar
        slow_mo=500       # 800ms de pausa entre cada ação
    )

    # Abre uma nova página
    page = browser.new_page()

    # Define o tamanho da janela do browser
    # width e height em pixels
    page.set_viewport_size({'width': 1280, 'height': 720})

    # Navega para o site — você verá o carregamento pausado
    page.goto('https://www.saucedemo.com')

    # Cada ação abaixo terá 800ms de pausa antes de executar
    # facilitando acompanhar visualmente

    # Clica no campo de usuário — verá o cursor piscar
    page.get_by_placeholder('Username').click()

    # Digita o usuário — verá cada letra aparecer com pausa
    page.get_by_placeholder('Username').fill('standard_user')

    # Clica no campo de senha
    page.get_by_placeholder('Password').click()

    # Digita a senha
    page.get_by_placeholder('Password').fill('secret_sauce')

    # Clica no botão de login — verá o clique acontecer
    page.get_by_role('button', name='Login').click()

    # Aguarda a página de produtos carregar
    page.wait_for_load_state('networkidle')

    # Imprime confirmação
    print(f'Login realizado! URL atual: {page.url}')

    # Fecha o browser
    browser.close()
