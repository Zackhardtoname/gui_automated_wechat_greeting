import itchat

groups = [
"波士顿-转租群-叁群",
"BU暑假转租群",
"波士顿-好租房-十三群",
"波士顿-好租房-十一",
"Boston留学活动群2018-2021",
"波士顿-转租群-二群",
"波士顿-好租房-十二群",
]

groups = [
"波士顿-二手交易群",
"【BU二手书交换群】",
"BU2021 本科新生官方群"
]

msg = """
Fenway 出家具，去年9月买的，很新
餐桌：30刀
椅子：9刀一把（共6个）
冰箱：100刀一个（共3个）
工作圆桌：50刀
床：100刀（全套，包括床垫等）
Wechat: Zackhardtoname
"""

itchat.auto_login(True)

all_groups = itchat.get_chatrooms(update=True)

for group in all_groups:
    if group["NickName"] in groups:
        print(group["NickName"])
        name = group["UserName"]
        print("send text")
        # itchat.send(text, name)
        print("send img")
        itchat.send_image("to_sell.png", name)
        # itchat.send_image("448_compressed.png", name)