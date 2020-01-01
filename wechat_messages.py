#coding=utf8
import pyperclip
import pyautogui
import time
import gen_img
import pickle
pyautogui.PAUSE = 1

with open('friends.pkl', 'rb') as f:
    friends = pickle.load(f)

def send_wishes_gui():
    for friend in friends:
        if ("sent" not in friend) and friend["NickName"] != "Zack Light":
            alias = friend["RemarkName"]
            username = friend["NickName"]

            name_to_use = alias if alias != "" else username
            print(name_to_use)

            # search
            pyautogui.click(270, 65)
            pyautogui.click(270, 65)
            to_search = friend["NickName"] + " " + friend["RemarkName"]
            pyperclip.copy(to_search)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.click(505, 205)

            # image
            generator = gen_img.Gen_Img()
            generator.gen_img(name_to_use)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(2)

            # wish
            wish = f'{name_to_use}, 祝您新年快乐!'
            pyperclip.copy(wish)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(2)
            pyautogui.press('enter')

            pyautogui.click(2542, 534)
            friend["sent"] = True

            with open('friends.pkl', 'wb') as f:
                pickle.dump(friends, f)

if __name__ == "__main__":
    send_wishes_gui()
