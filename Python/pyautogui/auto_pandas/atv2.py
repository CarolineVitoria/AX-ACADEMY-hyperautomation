import pyautogui as pa
import pandas as pd
import time
import os
import pygetwindow as gw
from datetime import datetime
from pathlib import Path
import subprocess

TITULOS_POSSIVEIS = ['notepad', 'bloco de notas']
PASTA_ATUAL = os.getcwd()
INTERVALO = 0.5
resultados = []

df = pd.read_excel("clientes.xlsx")

def verifica_notepad():
    janelas = gw.getAllWindows()
    for janela in janelas:
        for titulo in TITULOS_POSSIVEIS:
            if titulo.lower() in janela.title.lower():
                return janela
    return None

def abre_notepad():
    esta_aberto = verifica_notepad()
    time.sleep(1)
    if not esta_aberto:
        subprocess.Popen(["notepad.exe"])
        time.sleep(2)
        janela = verifica_notepad()
        if janela:
            janela.activate()
            time.sleep(1) 
        gera_relatorio()
    else:
        return None
    
def gera_relatorio():
    for index, row in df.iterrows():
        nome  = str(row["Nome"])
        email = str(row["Email"])
        cargo = str(row["Cargo"])
        telefone = str(row["Telefone"])
        pa.typewrite(f"Nome:  {nome}", interval=0.03)
        pa.press("enter")
        pa.typewrite(f"Email: {email}", interval=0.03)
        pa.press("enter")
        pa.typewrite(f"Telefone: {telefone}", interval=0.03)
        pa.press("enter")
        pa.typewrite(f"Cargo: {cargo}", interval=0.03)
        pa.press("enter")
        pa.press("enter")
        h = datetime.now().strftime("%Y%m%d_%H%M%S")

        resultados.append({
            "ID":     index + 1,
            "Nome":   nome,
            "Email":  email,
            "Telefone": telefone,
            "Cargo":  cargo,
            "Status": "Processado",
            "Horario": h
        })
        
    time.sleep(INTERVALO)

def nomeia_arquivo():
    desktop = Path.home() /"Documents"
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = desktop / f"PyAutoGUI-Pandas-{stamp}.xlsx"
    return nome_arquivo

def exportar_relatorio(resultados, caminho):
    df_saida = pd.DataFrame(resultados)
    df_saida.to_excel(caminho, index=False)
    print(f"\nRelatório salvo em: {caminho}")


abre_notepad()

print(resultados)

nome_arquivo = nomeia_arquivo()
exportar_relatorio(resultados, nome_arquivo)
