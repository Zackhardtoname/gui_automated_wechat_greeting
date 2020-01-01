#coding=utf8
import pyperclip
import pyautogui
import time
import gen_img
import pickle
pyautogui.PAUSE = 1

with open('friends.pkl', 'rb') as f:
    friends = pickle.load(f)

def send_wishes_gui(generator):
    for friend in friends:
        pyautogui.press('down')

        pyperclip.copy('no_alias')
        pyautogui.click(1053, 426, clicks=2, interval=.5) #alias
        pyautogui.hotkey('ctrl', 'c')
        alias = pyperclip.paste()

        pyautogui.click(922, 188, 2)  # username
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        username = pyperclip.paste()

        if alias == "no_alias":
            alias = username
        print(alias)

        name_to_use = alias if alias != "no_alias" else username

        generator.gen_img(name_to_use)
        for y in range(615, 800, 20):
            pyautogui.click(1111, y)

        pyautogui.hotkey('ctrl', 'v')
        time.sleep(2)

        wish = f'{name_to_use}, 祝您新年快乐!'
        pyperclip.copy(wish)
        pyautogui.hotkey('ctrl', 'v')

        pyautogui.press('enter')

        pyautogui.click(x=45, y=215) #contact list

if __name__ == "__main__":
    generator = gen_img.Gen_Img()
    send_wishes_gui(generator)
