# coding=utf8
import pyperclip
import pyautogui
from tqdm import tqdm
import gen_img
import pickle

pyautogui.PAUSE = 1
pause_time = 0
image_pause = 0

top_friend_position = (741, -1107)
alias_position = (2603, -1687)
username_position = (2445, -1951)
search_bar = (787, -2091)
first_search_res = (728, -1923)
id_position = (2614, -1558)


def copy_selection():
    pyperclip.copy("")
    pyautogui.hotkey('ctrl', 'c')
    val = pyperclip.paste()
    pyperclip.copy("")
    return val


def click(coords, numClicks=1):
    pyautogui.click(coords[0], coords[1], numClicks)


def get_friends():
    try:
        with open('friends.pkl', 'rb') as f:
            friends = pickle.load(f)
    except Exception as e:
        friends = []
        while len(friends) < 333:
            friend = {}
            # click(top_friend_position)
            click(alias_position, 2)
            pyautogui.hotkey('ctrl', 'a')
            friend['alias'] = copy_selection()
            click(username_position, 2)
            friend['username'] = copy_selection()
            print(friend)
            friends.append(friend)
            pyautogui.hotkey('shift', 'tab')
            pyautogui.press('down')

        with open('friends.pkl', 'wb') as f:
            pickle.dump(friends, f)

    return friends


def fuzzy_match(fn, confidence=.9):
    return pyautogui.locateCenterOnScreen(fn, confidence=confidence)


def check_logged_in():
    while (not fuzzy_match('./imgs/search_img.png')):
        confirm = fuzzy_match('./imgs/compressed.jpg') or fuzzy_match('./imgs/login_img.png')
        if confirm:
            pyautogui.click(confirm[0], confirm[1])
            pyautogui.click(confirm[0], confirm[1] + 100)
            pyautogui.hotkey('winleft', 'left')
            # pyautogui.hotkey('winleft', 'down')


def has_sent_img():
    return fuzzy_match('./imgs/2020_delete.png')


def paste_img(name_to_use):
    pyperclip.copy("")
    generator = gen_img.Gen_Img()
    generator.gen_img(name_to_use)
    pyautogui.hotkey('ctrl', 'v')


def paste_wish(name_to_use):
    pyperclip.copy("")
    wish = f'2021即将结束，回首过去，感恩遇见。\n\n毕业后我在西雅图亚马逊总部工作，感谢您过往的帮助!\n\n祝{name_to_use}2022年虎虎生威，欢愉胜意，万事可期!'
    pyperclip.copy(wish)
    pyautogui.hotkey('ctrl', 'v')


def send_wishes_gui():
    # missed = [""]
    skip = ["Zack Light", "A℡小袋鼠在线"]

    friends = get_friends()
    for i in tqdm(range(len(friends))):
        friend = friends[i]
        alias = friend["alias"]
        username = friend["username"]
        name_to_use = alias if alias != "" else username

        if name_to_use in skip or "sent" in friend:
            continue

        print(f"{name_to_use}")

        # search
        click(search_bar, 2)
        to_search = friend["alias"] + " " + friend["username"]
        # to_search = friend["id"]
        pyperclip.copy("")
        pyperclip.copy(to_search)
        pyautogui.hotkey('ctrl', 'v')
        click(first_search_res)

        # send
        pyperclip.copy("")
        paste_wish(name_to_use)
        paste_img(name_to_use)
        pyautogui.press('enter')
        friend["sent"] = True

        # check_logged_in()
        with open('friends.pkl', 'wb') as f:
            pickle.dump(friends, f)


if __name__ == "__main__":
    # get_friends()
    send_wishes_gui()
