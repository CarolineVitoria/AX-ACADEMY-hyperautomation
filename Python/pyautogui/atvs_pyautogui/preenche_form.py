import pyautogui
import time
import webbrowser
import pyperclip

print("Em 5 segundo iniciarei o preenchimento")
time.sleep(2)
url= 'http://localhost:8000/'


try:
    webbrowser.open(url)
    time.sleep(2)
    pyautogui.press('tab')
    time.sleep(2)
    pyautogui.write("Caroline")
    time.sleep(1)
    pyautogui.press('tab')
    pyautogui.write("eu@gmaail.com")
    pyautogui.press('tab')
    pyautogui.write("432.342.343-90")
    pyautogui.press('tab')
    pyautogui.write('8498891-3492')
    pyautogui.press('tab')
    pyautogui.write('Rodovia 66')
    pyautogui.press('tab')
    pyautogui.write('Manauscity')
    pyautogui.press('tab')
    pyautogui.press(['enter', 'down', 'enter', 'tab'])
    pyautogui.write('69033-560')
    pyautogui.press(['tab', 'enter'])
    pyautogui.press('down', 4)
    pyautogui.press(['enter', 'tab'])
    time.sleep(2)
    pyautogui.write('Observação: não tem observações ')
    time.sleep(1)

    #segunda parte
    # print("Ver posi")
    x, y = pyautogui.position()
    z_email, w_email =  2232, 404 #1553, 518
    x_obs, w_obs =  771, 974#1787, 1371 
    time.sleep(3)
    
    print("Posicão atual do mouse:", x, y)
    print("Posição email")

    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    txt_email = pyperclip.paste()
    pyautogui.press('tab', 8)
    pyautogui.write(txt_email)
    
    

    #terceira parte, preencher popup
    time.sleep(10)
    pyautogui.press('tab', 5)
    pyautogui.press('enter')
    pyautogui.write("n sei")
    pyautogui.press('tab')
    pyautogui.press('deve ser')
    pyautogui.press('tab')
    pyautogui.press('obs')
    box_email = pyautogui.locateAllOnScreen('btn_fechar.png', confidence=0.7)
    x, y = pyautogui.center(box_email)
    pyautogui.click(x, y)

except Exception as erro:   
    print("Erro", erro)

