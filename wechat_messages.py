#coding=utf8
import pyperclip
import pyautogui
import time
import gen_img
import pickle
pyautogui.PAUSE = 1
pause_time = 0
image_pause = 0

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

def fuzzy_match(fn, confidence=.9):
    return pyautogui.locateCenterOnScreen(fn, confidence=.9)

def check_logged_in():
    while(not fuzzy_match('./imgs/search_img.png')):
        confirm = fuzzy_match('./imgs/compressed.jpg') or fuzzy_match('./imgs/login_img.png')
        if confirm:
            pyautogui.click(confirm[0], confirm[1])
            pyautogui.click(confirm[0], confirm[1] + 100)

            time.sleep(pause_time)
            pyautogui.hotkey('winleft', 'left')
            # pyautogui.hotkey('winleft', 'down')

def has_sent_img():
    return fuzzy_match('./imgs/2020_msg_screenshot.png') or fuzzy_match('./imgs/2020_delete.png')

def paste_img(name_to_use):
    generator = gen_img.Gen_Img()
    generator.gen_img(name_to_use)
    pyautogui.hotkey('ctrl', 'v')

    time.sleep(pause_time + image_pause)

def paste_wish(name_to_use):
    wish = f'祝{name_to_use}2020新年快乐!'
    pyperclip.copy(wish)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(pause_time)

def send_wishes_gui():
    # missed = ["任朔禾"]
    skip = ["Zack Light"]
    total_num_friends = len(friends)

    for i in range(len(friends)):
        friend = friends[i]
        if "Checked" in friend:
            continue

        alias = friend["RemarkName"]
        username = friend["NickName"]
        name_to_use = alias if alias != "" else username

        if (name_to_use not in skip):
            print(f"{i}/{total_num_friends}: {name_to_use}")

            # search
            pyautogui.click(270, 65)
            pyautogui.click(270, 65)
            to_search = friend["NickName"] + " " + friend["RemarkName"]
            pyperclip.copy(to_search)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(pause_time)
            pyautogui.click(505, 205)

            if not has_sent_img():
                # Send
                pyperclip.copy("")
                paste_img(name_to_use)
                if "sent" not in friend:
                    paste_wish(name_to_use)
                else:
                    pyperclip.copy("补个图:)")
                    pyautogui.hotkey('ctrl', 'v')
                    time.sleep(pause_time)
                pyautogui.press('enter')

            friend["sent"] = True
            friend["Checked"] = True
            # check_logged_in()

            with open('friends.pkl', 'wb') as f:
                pickle.dump(friends, f)

if __name__ == "__main__":
    send_wishes_gui()
