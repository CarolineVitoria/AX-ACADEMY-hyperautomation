# Comparar headless vs headed

# Importa a API síncrona do Playwright
from playwright.sync_api import sync_playwright

# Importa datetime para medir o tempo de cada modo
from datetime import datetime

with sync_playwright() as p:

    # Modo headless

    print('Iniciando modo HEADLESS (sem janela)...')

    # Registra o tempo de início do modo headless
    inicio_headless = datetime.now()

    # Abre o browser SEM interface gráfica
    # headless=True é o padrão — aqui deixamos explícito para clareza
    browser_headless = p.chromium.launch(headless=True)

    # Abre uma nova página
    page_headless = browser_headless.new_page()

    # Navega para o site
    page_headless.goto('https://www.saucedemo.com')

    # Captura o título
    titulo = page_headless.title()

    # Calcula o tempo gasto
    tempo_headless = (datetime.now() - inicio_headless).total_seconds()

    print(f'  Título: {titulo}')
    print(f'  Tempo: {tempo_headless:.2f} segundos')

    # Fecha o browser headless
    browser_headless.close()

    # Modo headed

    print('\nIniciando modo HEADED (com janela)...')

    # Registra o tempo de início do modo headed
    inicio_headed = datetime.now()

    # Abre o browser COM interface gráfica
    # headless=False abre a janela do browser na tela
    browser_headed = p.chromium.launch(headless=False)

    # Abre uma nova página
    page_headed = browser_headed.new_page()

    # Navega para o site — você verá a janela abrir
    page_headed.goto('https://www.saucedemo.com')

    # Captura o título
    titulo = page_headed.title()

    # Calcula o tempo gasto
    tempo_headed = (datetime.now() - inicio_headed).total_seconds()

    print(f'  Título: {titulo}')
    print(f'  Tempo: {tempo_headed:.2f} segundos')

    # Fecha o browser headed
    browser_headed.close()

    # Comparação

    print(f'\nHeadless: {tempo_headless:.2f}s')
    print(f'Headed:   {tempo_headed:.2f}s')
    print(f'Diferença: {abs(tempo_headed - tempo_headless):.2f}s')