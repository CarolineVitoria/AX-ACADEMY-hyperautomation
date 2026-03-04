import pyautogui
import time

time.sleep(2)

#salvar a tela inteira em um arq
pyautogui.screenshot('tela.png')

#retorna a imagem sem salvar
img = pyautogui.screenshot()
print(type(img))

#capturar só uma região (x, y, largura, altura)
pyautogui.screenshot('canto.png', region=(0, 0, 400, 300))