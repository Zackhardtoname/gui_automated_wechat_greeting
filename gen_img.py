from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import win32clipboard
from io import BytesIO

class Gen_Img():
    def __init__(self):
        self.font_family = "font_families/YiPinQingYeShouXieTi-2.ttf"
        self.header_font_size = 70
        self.header_font = ImageFont.truetype(self.font_family, self.header_font_size)
        self.body_footer_font_size = int(self.header_font_size * .9)
        self.msg_font = ImageFont.truetype(self.font_family, self.body_footer_font_size)
        self.footer_font = ImageFont.truetype(self.font_family, self.body_footer_font_size)

        self.img = Image.open("./imgs/lunar_new_year.png")
        self.font_color = "black"
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

        line_separation = 20
        self.cur_pos = (cur_w, cur_h + line_separation)
        self.draw.text(self.cur_pos, text, font=self.cur_font, fill=self.font_color)

    def gen_img(self, RemarkName=""):
        header = "祝" + RemarkName + "，"
        msg = u"感恩遇见！感谢帮助！"
        msg2 = u"祝新的一年，美好相随，事事顺意！"
        footer = u"刘建萍"
        # footer2 = u"zackLight.com"

        self.draw = ImageDraw.Draw(self.img)
        self.cur_pos = (self.W // 10, self.H // 2.5)

        self.cur_font = self.header_font
        self.draw.text(self.cur_pos, header, font=self.cur_font, fill=self.font_color)

        self.update_pos_and_font(next_font=self.msg_font, text=msg)
        self.update_pos_and_font(next_font=self.msg_font, text=msg2)
        self.update_pos_and_font(next_font=self.footer_font, text=footer)
        # self.update_pos_and_font(next_font=self.footer_font, text=footer2)



        output = BytesIO()
        self.img.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()

        self.send_to_clipboard(win32clipboard.CF_DIB, data)

if __name__ == "__main__":
    generator = Gen_Img()
    generator.gen_img("您")