import subprocess
import pyautogui
import time
from pathlib import Path
from datetime import datetime

def so_quando_tiver_ativo():
    titulos_possiveis = ['Bloco de Notas', 'Notepad']

    print('Aguardando o Notepad abrir... (Ctrl+C para parar)')

    while True:
        return True

        if notepad_aberto:
            print('Notepad está aberto. Saindo do bot.')
            break

    time.sleep(0.5)
    
# Inicia um processo (ex: listar arquivos no Linux)
processo = subprocess.Popen(["notepad.exe"])
time.sleep(1)

pyautogui.write("lalalala")
pyautogui.hotkey('ctrl', 's')
desktop = Path.home() / "Documents"
stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
arquivo_txt = desktop / f"my_own_summer_{stamp}.txt"

pyautogui.write(str(arquivo_txt))
time.sleep(0.2)
pyautogui.press("enter")
time.sleep(1.0)
# Fechar Bloco de Notas

pyautogui.hotkey("alt", "f4")
pyautogui.press("s")
time.sleep(0.3)

