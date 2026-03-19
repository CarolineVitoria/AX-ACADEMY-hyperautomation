import subprocess
import pyautogui
import time
from pathlib import Path
from datetime import datetime
import pygetwindow as gw  

titulos_possiveis = ['Bloco de Notas', 'Notepad']


def notepad_esta_aberto():
    janelas = gw.getWindowsWithTitle('')
    for janela in janelas:
        for titulo in titulos_possiveis:
            if titulo.lower() in janela.title.lower():
                return janela
    return None


processo = subprocess.Popen(["notepad.exe"])

print("Aguardando Notepad abrir...")
janela_notepad = None
while janela_notepad is None:
    janela_notepad = notepad_esta_aberto()
    time.sleep(0.5)

print(f"Notepad aberto: {janela_notepad.title}")


desktop = Path.home() / "Documents"
stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
arquivo_txt = desktop / f"my_own_summer_{stamp}.txt"
snapshot_path = desktop / f"snapshot_{stamp}.png"


pyautogui.write("lalalala")


pyautogui.screenshot(str(snapshot_path))
print(f"Snapshot salvo em: {snapshot_path}")


pyautogui.hotkey('ctrl', 's')
time.sleep(0.5)
pyautogui.write(str(arquivo_txt))
pyautogui.press("enter")
time.sleep(1)


pyautogui.hotkey("alt", "f4")
pyautogui.press("s")
time.sleep(0.3)