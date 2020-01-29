#coding=utf8
import pyperclip
import pyautogui
from tqdm import tqdm
import gen_img
import time
import pickle
pyautogui.PAUSE = 1
pause_time = 0
image_pause = 0

def get_friends():
    try:
        with open('friends.pkl', 'rb') as f:
            friends = pickle.load(f)
    except Exception as e:
        print(e)
        import itchat
        itchat.auto_login()
        friends = itchat.get_friends(update=False)[1:]
        with open('friends.pkl', 'wb') as f:
            pickle.dump(friends, f)
    return friends

def fuzzy_match(fn, confidence=.9):
    return pyautogui.locateCenterOnScreen(fn, confidence=confidence)

def check_logged_in():
    while(not fuzzy_match('./imgs/search_img.png')):
        confirm = fuzzy_match('./imgs/compressed.jpg') or fuzzy_match('./imgs/login_img.png')
        if confirm:
            pyautogui.click(confirm[0], confirm[1])
            pyautogui.click(confirm[0], confirm[1] + 100)
            pyautogui.hotkey('winleft', 'left')
            # pyautogui.hotkey('winleft', 'down')

def has_sent_img():
    return fuzzy_match('./imgs/2020_delete.png')

def paste_img(name_to_use):
    generator = gen_img.Gen_Img()
    generator.gen_img(name_to_use)
    pyautogui.hotkey('ctrl', 'v')

def paste_wish(name_to_use):
    wish = f'祝{name_to_use}2020新年快乐!'
    pyperclip.copy(wish)
    pyautogui.hotkey('ctrl', 'v')

def send_wishes_gui():
    # missed = [""]
    skip = ["Zack Light"]

    friends = get_friends()
    for i in tqdm(range(len(friends))):
        friend = friends[i]
        alias = friend["RemarkName"]
        username = friend["NickName"]
        name_to_use = alias if alias != "" else username

        if (name_to_use in skip):
            continue

        print(f"{name_to_use}")

        # search
        pyautogui.click(270, 65)
        pyautogui.click(270, 65)
        to_search = friend["NickName"] + " " + friend["RemarkName"]
        pyperclip.copy(to_search)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.click(505, 205)

        if not has_sent_img():
            pyperclip.copy("")
            paste_img(name_to_use)

            if "sent" not in friend:
                paste_wish(name_to_use)
            else:
                pyperclip.copy("补个图:)")
                pyautogui.hotkey('ctrl', 'v')

            pyautogui.press('enter')
        else:
            friend["Checked"] = True

        friend["sent"] = True

        check_logged_in()
        with open('friends.pkl', 'wb') as f:
            pickle.dump(friends, f)

if __name__ == "__main__":
    # time.sleep(60 * 60 * 5)
    send_wishes_gui()
