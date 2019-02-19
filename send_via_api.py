def send_wishes():
    friendList = itchat.get_friends(update=False)[1:]
    for i in range(len(friendList[40:])):
        friend = friendList[i+40]
        print("R: " + friend['RemarkName'])
        print("N: " + friend['NickName'])
        lan_option = input("Language: ")
        friendList[i]["lan"] = lan_option

        if lan_option == "":
            continue
        elif lan_option == "c":
            s = c_wish
        elif lan_option == "e":
            s = e_wish

        name_opt = input("Name: ")
        if name_opt == "r":
            wish = s % friend['RemarkName']
        elif name_opt == "n":
            wish = s % friend['NickName']
        else:
            wish = s % name_opt
        print(wish)
        # itchat.send(wish, friend["UserName"])
        # itchat.send_image("./card.png", friend["UserName"])