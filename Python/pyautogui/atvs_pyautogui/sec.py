import time
from pathlib import Path
from datetime import datetime
import pyautogui as pag

pag.FAILSAFE = True
pag.PAUSE = 0.2

print("Começando em 3 segundos...")
time.sleep(3)

pag.hotkey("win", "r")
time.sleep(0.8)
pag.write("notepad")
pag.press("enter")
time.sleep(1.2)

agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
mensagem = "Estudo de caso RPA - Windows + PyAutoGUI\n"
pag.write(mensagem, interval=0.01)
time.sleep(0.3)

desktop = Path.home() / "Documents"
stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
arquivo_txt = desktop / f"caso_rpa_notepad_{stamp}.txt"

pag.hotkey("ctrl", "shift", "s")
time.sleep(1.0)

pag.write(str(arquivo_txt))
time.sleep(0.2)
pag.press("enter")
time.sleep(1.0)

pag.hotkey("alt", "a")
pag.press("s")
time.sleep(0.3)

print("Concluído.")
print("Arquivo TXT:", arquivo_txt)