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
alias_position = (2736, -1909)
bottom_friend_position = (1018, -67)
username_position = (2445, -1951)
search_bar = (892, -2097)
first_search_res = (1069, -1935)
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

        for _ in range(377):
            friend = {}
            # click(top_friend_position)
            click(alias_position, 2)
            # pyautogui.hotkey('ctrl', 'a')
            friend['alias'] = copy_selection()
            # click(username_position, 2)
            friend['username'] = friend['alias']
            print(friend)
            friends.append(friend)
            # pyautogui.hotkey('shift', 'tab')
            click(bottom_friend_position, 1)
            pyautogui.press('down')

        aliases = {friend["alias"]: None for friend in friends if friend["alias"]}
        unique = []

        for alias in aliases:
            people = [friend for friend in friends if friend["alias"] == alias]
            unique.append(people[0])

        with open('friends.pkl', 'wb') as f:
            pickle.dump(unique, f)

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
    wish = f'祝{name_to_use}福兔迎祥! 感谢您给予的帮助!\n\nzackLight.com'
    pyperclip.copy(wish)
    pyautogui.hotkey('ctrl', 'v')


def send_wishes_gui():
    # missed = [""]
    skip = ["Zack Light", "A℡小袋鼠在线"]
    friends = get_friends()

    for i in tqdm(range(len(friends))):
        friend = friends[i]
        name_to_use = friend["alias"]

        if name_to_use in skip or "sent" in friend:
            continue

        print(f"{name_to_use}")

        # search
        click(search_bar, 2)
        pyperclip.copy("")
        pyperclip.copy(name_to_use)
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
