
import pyautogui
import pandas as pd
import time
import os
PASTA_ATUAL = os.getcwd()


PLANILHA_ENTRADA = "clientes.xlsx"
PLANILHA_SAIDA = "clientes_processados.xlsx"
INTERVALO = 0.5  # segundos entre ações

df = pd.read_excel(PLANILHA_ENTRADA)

resultados = []

for index, row in df.iterrows():
    nome = str(row["Nome"])
    email = str(row["Email"])
    cargo = str(row["Cargo"])

    pyautogui.hotkey("win", "r")
    time.sleep(INTERVALO)
    pyautogui.typewrite("notepad", interval=0.05)
    pyautogui.press("enter")
    time.sleep(1)

    pyautogui.typewrite(f"Nome:  {nome}", interval=0.03)
    pyautogui.press("enter")
    pyautogui.typewrite(f"Email: {email}", interval=0.03)
    pyautogui.press("enter")
    pyautogui.typewrite(f"Cargo: {cargo}", interval=0.03)
    pyautogui.press("enter")
    time.sleep(INTERVALO)

    pyautogui.hotkey("ctrl", "s")
    time.sleep(INTERVALO)
    pyautogui.typewrite(os.path.join(PASTA_ATUAL, f"ficha_{index+1}.txt"), interval=0.05)
    pyautogui.press("enter")
    time.sleep(INTERVALO)
    pyautogui.hotkey("alt", "f4")
    time.sleep(INTERVALO)

    resultados.append({
        "ID": index + 1,
        "Nome": nome,
        "Email": email,
        "Cargo": cargo,
        "Status": "Processado"
    })
    print(f"[OK] Linha {index + 1}: {nome}")

df_saida = pd.DataFrame(resultados)
df_saida.to_excel(PLANILHA_SAIDA, index=False)
print(f"\nRelatório salvo em: {PLANILHA_SAIDA}")