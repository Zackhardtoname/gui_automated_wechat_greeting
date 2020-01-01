from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import win32clipboard
from io import BytesIO

class Gen_Img():
    def __init__(self):
        self.font_family = "./font_families/PangMenZhengDaoCuShuTi-2.ttf"
        self.header_font_size = 90
        self.header_font = ImageFont.truetype(self.font_family, self.header_font_size)
        self.body_footer_font_size = int(self.header_font_size * .9)
        self.msg_font = ImageFont.truetype(self.font_family, self.body_footer_font_size)
        self.footer_font = ImageFont.truetype(self.font_family, self.body_footer_font_size)

        self.img = Image.open("./imgs/paper_lantern.jpg")
        self.font_color = "white"
        self.W, self.H = self.img.size

    def send_to_clipboard(self, clip_type, data):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(clip_type, data)
        win32clipboard.CloseClipboard()

    def update_pos_and_font(self, next_font, text):
        prev_font = self.cur_font
        prev_size = self.draw.textsize(text, font=prev_font)
        cur_size = self.draw.textsize(text, font=next_font)
        cur_w, cur_h = self.cur_pos
        cur_h = self.cur_pos[1] + prev_size[1]

        # body indentation
        if prev_font == self.header_font:
            cur_w += self.W // 10
            cur_h += self.H // 10

        # footer right alignment
        if next_font == self.footer_font and self.cur_font != self.footer_font:
            cur_w = self.W - cur_size[0] - self.W // 8
            cur_h += self.H // 12

        # update font
        self.cur_font = next_font

        self.cur_pos = (cur_w, cur_h)
        self.draw.text(self.cur_pos, text, font=self.cur_font, fill=self.font_color)

    def gen_img(self, RemarkName=""):
        header = "亲爱的" + RemarkName + "，"
        msg = u"感谢您陪我度过难忘温暖的2019，"
        msg2 = u"祝您在2020年万事如意！"
        footer = u"Zack (张羿)"
        footer2 = u"zackLight.com"

        self.draw = ImageDraw.Draw(self.img)
        self.cur_pos = (self.W // 8, self.H // 5)

        self.cur_font = self.header_font
        self.draw.text(self.cur_pos, header, font=self.cur_font, fill=self.font_color)

        self.update_pos_and_font(next_font=self.msg_font, text=msg)
        self.update_pos_and_font(next_font=self.msg_font, text=msg2)
        self.update_pos_and_font(next_font=self.footer_font, text=footer)
        self.update_pos_and_font(next_font=self.footer_font, text=footer2)

        # cur_pos = self.update_pos_and_font(cur_pos, font, msg)
        # self.draw.text(self.cur_pos, footer2, font=font, fill=self.font_color)

        self.img.save(f'./cards/{RemarkName}.jpg')
        filepath = f'./cards/{RemarkName}.jpg'
        image = Image.open(filepath)

        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()

        self.send_to_clipboard(win32clipboard.CF_DIB, data)

if __name__ == "__main__":
    generator = Gen_Img()
    generator.gen_img("Zack")