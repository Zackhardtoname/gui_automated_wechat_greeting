# coding=utf8
from sys import stderr

import pyperclip
import pyautogui
from tqdm import tqdm
import gen_img
import pickle

year = 2024
pyautogui.PAUSE = 1
pause_time = 0
image_pause = 0

top_friend_position = (1002, -1107)
# username is the remark/alias if set otherwise the name the user has chosen
username_position = (2736, -1909)
bottom_friend_position = (1018, -67)
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
    # Get a list of current friends and save results into a file locally
    # Every year, delete the pkl file before the process
    try:
        with open(f'{year}_friends.pkl', 'rb') as f:
            friends = pickle.load(f)
    except FileNotFoundError:
        friends = []
        click(top_friend_position)
        # hard coded num of friends, so you don't need to detect end of friend list
        num_friends = 388
        for _ in tqdm(range(num_friends)):
            friend = {}
            click(username_position, 2)
            friend['username'] = copy_selection()
            print(friend)
            friends.append(friend)
            # Get back to the friend list
            for _ in range(2):
                pyautogui.hotkey('shift', 'tab')
            pyautogui.press('down')

        # dedup
        usernames = {friend["username"] for friend in friends if friend["username"]}
        unique = []

        for username in usernames:
            people = [friend for friend in friends if friend["username"] == username]
            if len(people) > 1:
                print(f"WARNING: {len(people)}", file=stderr)
            unique.append(people[0])

        with open('friends.pkl', 'wb') as f:
            pickle.dump(unique, f)

    return friends


def paste_img(name_to_use):
    pyperclip.copy("")
    generator = gen_img.Gen_Img()
    generator.gen_img(name_to_use)
    pyautogui.hotkey('ctrl', 'v')


def paste_wish(name_to_use):
    pyperclip.copy("")
    wish = f'祝{name_to_use}龙腾四海，瑞气盈门! 感谢过去一年里您的帮助!\n\nzackLight.com'
    pyperclip.copy(wish)
    pyautogui.hotkey('ctrl', 'v')


def send_wishes_gui():
    # missed = [""]
    skip = ["Zack Light"]
    friends = get_friends()

    for i in tqdm(range(len(friends))):
        friend = friends[i]
        name_to_use = friend["username"]

        if not friend or name_to_use in skip or "sent" in friend:
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
    get_friends()
    send_wishes_gui()
