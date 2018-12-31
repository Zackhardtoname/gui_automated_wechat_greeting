#coding=utf8
# import itchat
import pyperclip
import pyautogui
import time
# pyautogui.PAUSE = 0.4

c_wish = u'祝%s新年快乐！圣诞快乐！'
e_wish = u'Hi %s Happy Holidays!'

# def send_wishes():
#     friendList = itchat.get_friends(update=False)[1:]
#     for i in range(len(friendList[40:])):
#         friend = friendList[i+40]
#         print("R: " + friend['RemarkName'])
#         print("N: " + friend['NickName'])
#         lan_option = input("Language: ")
#         friendList[i]["lan"] = lan_option
#
#         if lan_option == "":
#             continue
#         elif lan_option == "c":
#             s = c_wish
#         elif lan_option == "e":
#             s = e_wish
#
#         name_opt = input("Name: ")
#         if name_opt == "r":
#             wish = s % friend['RemarkName']
#         elif name_opt == "n":
#             wish = s % friend['NickName']
#         else:
#             wish = s % name_opt
#         print(wish)
#         # itchat.send(wish, friend["UserName"])
#         # itchat.send_image("./card.png", friend["UserName"])

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
        pyautogui.press('down')
        pyautogui.click(2054, 1950)
        # send = input("Send: ")
        # if send == " ":
        #     pyautogui.click(278, 2060)
        #     pyautogui.click(235, 1931)
        #     pyautogui.click(278, 2060)
        #
        #     continue
        pyautogui.click(1041, 359) #r
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')

        RemarkName = pyperclip.paste()
        pyautogui.click(925, 163, 2) #NickName
        pyautogui.hotkey('ctrl', 'c')
        NickName = pyperclip.paste()

        pyautogui.click(x=1189, y=620) #message btn
        pyautogui.click(x=1189, y=668) #message btn loc 2

        pyautogui.click(2054, 1950)
        wish = contruct_wish(RemarkName, NickName)
        pyautogui.click(1193, 1993)

        if wish != None:
            print(wish)
            pyperclip.copy(wish)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(.1)
            pyautogui.press('enter')
            pyautogui.hotkey('ctrl', 'win', '1')  # ctrl-v to paste
            time.sleep(.3)
            pyautogui.press('enter')
        pyautogui.click(x=45, y=215) #contact list

# itchat.auto_login(True)

send_wishes_gui()