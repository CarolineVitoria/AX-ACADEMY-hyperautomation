import pyautogui
import time

print("Em 3s procurarei a calculadora")
time.sleep(4)

try:
    box = pyautogui.locateOnScreen('calculadora.png', confidence=0.7)
    x, y = pyautogui.center(box)
    pyautogui.click(x, y)
    print('Cliquei na calculadora')
except pyautogui.ImageNotFoundException:
    print('Não achei a calculadora na tela.')
    