import pandas as pd
import numpy as np
from playwright.sync_api import sync_playwright
import time
from datetime import datetime
from pathlib import Path

CONTADOR_REGISTROS = 0
RELATORIO_NOMES_SUCESSO = []


nomes = ["Vitória", "oi Beria", "Rodrigues", "Beatrix", "Mamba Negra",
         "Ana", "Obi", "Anakin", "Padmé", "Carmilla"]


np.random.seed(42) 

senhas = np.random.choice(["abc123", "senha123", "1qwerty", "pass2024", "123456a", "SenhaTest3!", "SenhaTest3q!", "SeqnhaTest3!", "SeqnhaTest3!", "SqenhaTest3!"])
descricoes = np.random.choice(["Usuário novo", "Cliente VIP", "Administrador", "Visitante"], 10)
imoveis = np.random.choice(["One", "Two", "Three"], 10)
cidades = np.random.choice(["San Francisco", "New York", "Seattle", "Los Angeles", "Chicago"], 10)


datas = pd.date_range(start="2020-01-01", end="2025-12-31", periods=10)
datas = datas.strftime("%d/%m/%Y")


df = pd.DataFrame({
    "Nome": nomes,
    "Senha": senhas,
    "Desc": descricoes,
    "Qtd_imoveis": imoveis,
    "Cidade": cidades,
    "Data": datas
})


print(df)

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        "./user-data",
        headless=False,
        slow_mo=500,
        permissions=["clipboard-read", "clipboard-write"],
        chromium_sandbox=False,
    )

    page = browser.new_page()
    page.goto('https://www.selenium.dev/selenium/web/web-form.html')
    page.wait_for_load_state('networkidle')
    locator_name = page.locator("#my-text-id")
    locator_password = page.locator("input[type=password]")
    locator_text = page.locator("textarea[name=my-textarea]")
    locator_dropdown = page.locator("select[name=my-select]")
    dropdown_datalist = page.locator("input[name=my-datalist]")
    locator_datapicker = page.locator("input[name=my-date]")
    locator_submit = page.locator("button[type=submit]")
    locator_recebido = page.locator("#message")

    for row in df.itertuples():
        
        locator_name.type(row.Nome, delay=10)
        locator_password.type(row.Senha, delay=10)
        locator_text.type(row.Desc)
        locator_dropdown.click()
        locator_dropdown.select_option(row.Qtd_imoveis)
        dropdown_datalist.click()
        input_cidade = page.locator('input[list="my-options"]')
        input_cidade.fill(row.Cidade)
        locator_datapicker.fill(row.Data)
        time.sleep(2)
        CONTADOR_REGISTROS+=1
        page.screenshot(path=f'form {CONTADOR_REGISTROS}.png')
        print('Screenshot da atv salvo')
        locator_submit.click()
        time.sleep(2)
        print(locator_recebido.inner_text())
        if(locator_recebido.inner_text() == "Received!"):
            RELATORIO_NOMES_SUCESSO.append(f'{row.Nome} : Sucesso')
            page.screenshot(path=f'form_preenchido-{CONTADOR_REGISTROS}.png')
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            print(f'sucesso - {stamp}')
        else:
            RELATORIO_NOMES_SUCESSO.append(f'{row.Nome} : Falha')
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            print(f' falha - {stamp}')
        page.go_back()
        page.reload()
        page.wait_for_load_state("networkidle") 


with open("relatorio.txt", "w", encoding="utf-8") as f:
    f.write(f"Relatório de nomes recebidos \n")
    f.write("-------------------------------\n")
    for nome in RELATORIO_NOMES_SUCESSO:
        f.write(f"{nome}\n")
