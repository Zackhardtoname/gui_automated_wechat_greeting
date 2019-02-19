#coding=utf8
# import itchat
import pyperclip
import pyautogui
import time
import gen_img
pyautogui.PAUSE = 1

c_wish = u'祝%s新年快乐！圣诞快乐！'
e_wish = u'Hi %s Happy Holidays!'

def contruct_wish(RemarkName, NickName):
    print("R: " + RemarkName)
    print("N: " + NickName)
    lan_option = input("Language: ")
    # friendList[i]["lan"] = lan_option

    if lan_option == "c":
        s = c_wish
    elif lan_option == "e":
        s = e_wish
    else:
        return None

    name_opt = input("Name: ")
    if name_opt == "r":
        wish = s % RemarkName
    elif name_opt == "n":
        wish = s % NickName
    elif name_opt == "f":
        wish = s % NickName[1:]
    elif name_opt == "j":
        wish = s % (NickName[1:] + "姐")
    elif name_opt == "g":
        wish = s % (NickName[1:] + "哥")
    else:
        wish = s % name_opt
    return wish

def send_wishes_gui():
    while True:
        pyperclip.copy('Hi')
        pyautogui.press('down')
        # pyautogui.click(2054, 1950)
        # send = input("Send: ")
        # if send == " ":
        #     pyautogui.click(278, 2060)
        #     pyautogui.click(235, 1931)
        #     pyautogui.click(278, 2060)
        #
        #     continue

        pyautogui.click(1053, 426, clicks=2, interval=.5) #r
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        RemarkName = pyperclip.paste()

        pyautogui.click(922, 188, 2)  # NickName
        pyautogui.hotkey('ctrl', 'c')
        NickName = pyperclip.paste()
        if NickName == '紫林':
            return
        if RemarkName == "Hi":
            RemarkName = NickName
        print(RemarkName)

        #
        # pyautogui.click(x=1189, y=620) #message btn
        # pyautogui.click(x=1189, y=668) #message btn loc 2
        #
        # pyautogui.click(2054, 1950)
        # wish = contruct_wish(RemarkName, NickName)

        gen_img.gen_img(RemarkName)
        for y in range(615, 800, 20):
            pyautogui.click(1111, y)
        # res = pyautogui.locateOnScreen('msg_2.jpg')
        # if not res:
        #     res = []
        #     res.append(1214)
        #     res.append(703)
        # pyautogui.click(res[0], res[1]) #msg

        # if wish != None:
        # print(wish)
        # pyperclip.copy(wish)
        pyautogui.click(996, 1786) #contact list
        # time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        pyautogui.press('enter')
        # pyautogui.hotkey('ctrl', 'win', '1')  # ctrl-v to paste
        # time.sleep(.3)
        # pyautogui.press('enter')
        pyautogui.click(x=45, y=215) #contact list

# itchat.auto_login(True)

send_wishes_gui()