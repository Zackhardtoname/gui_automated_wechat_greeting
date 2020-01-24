#coding=utf8
import pyperclip
import pyautogui
import time
import gen_img
import pickle
pyautogui.PAUSE = 1
pause_time = 1

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

def check_logged_in():
    while(not pyautogui.locateCenterOnScreen('./search_img.png')):
        confirm = pyautogui.locateCenterOnScreen('./compromised_img.png') or pyautogui.locateCenterOnScreen('./login_img.png')
        if confirm:
            pyautogui.click(confirm[0], confirm[1])
            pyautogui.click(confirm[0], confirm[1] + 100)

            time.sleep(3)
            pyautogui.hotkey('winleft', 'left')

            # pyautogui.hotkey('winleft', 'down')

def send_wishes_gui():
    delay = False
    missed = []
    skip = ["Zack Light"]

    for i in range(len(friends)):
        friend = friends[i]

        alias = friend["RemarkName"]
        username = friend["NickName"]
        name_to_use = alias if alias != "" else username

        if delay:
            delay = not (name_to_use in missed)
            if delay:
                continue

        if (("sent" not in friend)) and (name_to_use not in skip):
            print(f"{i}: {name_to_use}")

            # search
            pyautogui.click(270, 65)
            pyautogui.click(270, 65)
            to_search = friend["NickName"] + " " + friend["RemarkName"]
            pyperclip.copy(to_search)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.click(505, 205)
            pyperclip.copy("")

            # image
            generator = gen_img.Gen_Img()
            generator.gen_img(name_to_use)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(pause_time)

            # wish
            wish = f'祝{name_to_use}新年快乐!'
            pyperclip.copy(wish)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(pause_time)
            pyautogui.press('enter')

            friend["sent"] = True

            check_logged_in()

            with open('friends.pkl', 'wb') as f:
                pickle.dump(friends, f)

if __name__ == "__main__":
    send_wishes_gui()
