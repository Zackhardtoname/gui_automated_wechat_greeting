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

    img = Image.open("bd.jpg")

    W, H = img.size
    header = RemarkName + "，"
    if RemarkName != "Hi":
        header = "Dear " + header
    msg = u"May the van de graaff generators be with u everyday!"
    msg2 = u"Wishing you a very happy birthday!"
    footer = u"SAIL"
    footer2 = u"https://sail.bu.edu"

    draw = ImageDraw.Draw(img)
    header_font = ImageFont.truetype("YiPinQingYeShouXieTi-2.ttf", 68)
    msg_font = ImageFont.truetype("YiPinQingYeShouXieTi-2.ttf", 58)
    footer_font = ImageFont.truetype("YiPinQingYeShouXieTi-2.ttf", 58)

    w, h = draw.textsize(msg, font=msg_font)

    footer_offset = -650
    msg_offset = 20

    draw.text(((W-w)/2, H/2-80), header, fill="black", font=header_font)
    draw.text(((W-w)/2 + msg_offset, (H-h)/2+70), msg, fill="black", font=msg_font)
    draw.text(((W-w)/2 + msg_offset, (H-h)/2 + 150), msg2, fill="black", font=msg_font)
    # draw.text(((W-w)/2 - 150,(H-h)/2 + 160), msg3, fill="black", prev_font=msg_font)
    draw.text((W + footer_offset, H - 200), footer, fill="black", font=footer_font)
    draw.text((W + footer_offset, H - 250), footer2, fill="black", font=footer_font)

    img.save('./cards/{Remarkname}.jpg')

    filepath = './cards/{Remarkname}.jpg'
    image = Image.open(filepath)

    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()

    send_to_clipboard(win32clipboard.CF_DIB, data)

if __name__ == "__main__":
    gen_img("Shreya")