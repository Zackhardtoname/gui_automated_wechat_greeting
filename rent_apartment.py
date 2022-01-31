import itchat

groups = [
"UMCSSA 2019 房屋＋二手群",
# "UMCSSA 2019 秋季新生群",
# "【Willowtree 💛】",
# "UM EECS + UMSI",
# "Hub🐺",
# "UM 数学 | 统计 | 数据科学",
# "UMich19winter新生群",
# "UMCSSA 2019 转学生答疑群",
]

itchat.auto_login(True)

all_groups = itchat.get_chatrooms(update=True)
text = "Willowtree 1 bedroom 1 bath apartment available from 7/7 to 7/31 (negotiable) for $700"
img_path = "all.png"

for group in all_groups:
    if group["NickName"] in groups:
        print(group["NickName"])
        name = group["UserName"]
        print("send text")
        itchat.send(text, name)
        print("send img")
        itchat.send_image(img_path, name)
