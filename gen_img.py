from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import win32clipboard
from io import BytesIO

def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()

def gen_img(RemarkName="Hi"):

    img = Image.open("lunar_new_year.png")

    W, H = img.size
    header = RemarkName + "，"
    if RemarkName != "Hi":
        header = "亲爱的" + header
    msg = u"原本写了很多，删减后只剩了一句。"
    msg2 = u"愿你有诗也有酒；有最执着的梦想，也有最洒脱的生活。"
    footer = u"Zack(张羿)"
    footer2 = u"zackLight.com"

    draw = ImageDraw.Draw(img)
    header_font = ImageFont.truetype("YiPinQingYeShouXieTi-2.ttf", 68)
    msg_font = ImageFont.truetype("YiPinQingYeShouXieTi-2.ttf", 58)
    footer_font = ImageFont.truetype("YiPinQingYeShouXieTi-2.ttf", 58)

    w, h = draw.textsize(msg, font=msg_font)

    draw.text(((W-w)/2 - 290, H/2-80), header, fill="black", font=header_font)
    draw.text(((W-w)/2 - 290,(H-h)/2+70), msg, fill="black", font=msg_font)
    draw.text(((W-w)/2 - 290,(H-h)/2 + 150), msg2, fill="black", font=msg_font)
    # draw.text(((W-w)/2 - 150,(H-h)/2 + 160), msg3, fill="black", font=msg_font)
    draw.text((W - 500,H - 200), footer, fill="black", font=footer_font)
    draw.text((W - 500,H - 250), footer2, fill="black", font=footer_font)

    img.save('./cards/{Remarkname}.jpg')

    filepath = './cards/{Remarkname}.jpg'
    image = Image.open(filepath)

    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()

    send_to_clipboard(win32clipboard.CF_DIB, data)

# if __name__ == "__main__":
#     gen_img("Zack")