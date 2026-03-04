import pyautogui
import time
import pandas as pd

df_csv = pd.read_csv(
    './../pandas/entrada.csv',
    sep=',',
    encoding='utf-8',
    dtype={'categoria': 'string'}
)
print(df_csv)

qtd = 3
intervalo = 3

largura, altura = pyautogui.size() #pega a resolução da tela
print('Tela:', largura, 'x', altura)

i = 1
x, y = pyautogui.position() #pega posição do mouser
print('Leitura', i, '->Mouse em', x, y)
pyautogui.click(1400, 600)
pyautogui.press('shift')
with pyautogui.hold('shift'):
    pyautogui.write('abracadabra')
    pyautogui.press(['a'])
    pyautogui.press(['b'])
    pyautogui.press(['r'])
    pyautogui.press(['a'])
    pyautogui.press(['c'])
    pyautogui.press(['a'])
    pyautogui.press(['d'])
    pyautogui.press(['a'])
    pyautogui.press(['b'])
    pyautogui.press(['r'])
    pyautogui.press(['a'])




while i < qtd:
    print("Mova seu mouse para outra posição em até", str(intervalo)+ 's')
    time.sleep(intervalo)
    i += 1
    x,y = pyautogui.position()
    print('Leitura', i, '->Mouse em:', x, y)
    espacamento = 100
    pyautogui.moveTo(x, (y+100))
    #pyautogui.click()
    #pyautogui.write("nome eu eu")
    #pyautogui.press('tab')
    #presstab


    