import pyautogui
import time

print("Em 3 segs eu irei procurar os icons")

try:
    icons = list(pyautogui.locateAllOnScreen('icon.png', confidence=0.9, grayscale=True))
    print("Quantidade encontrada:", len(icons))
except pyautogui.ImageNotFoundException:
    print("Não encontrada")