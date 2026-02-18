import asyncio
import json
import os
import logging
from typing import Dict, List, Optional
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO

from wechaty import Wechaty, Contact, Message
from wechaty_puppet import ScanStatus
from filebox import FileBox
import qrcode_terminal

# Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class ImageGenerator:
    def __init__(self):
        # Using the same font as in the original script
        self.font_family = "font_families/字小魂国风少年体.ttf"
        self.header_font_size = 45
        self.line_separation = 0
        
        if not os.path.exists('cards'):
            os.makedirs('cards')

        try:
            self.header_font = ImageFont.truetype(self.font_family, self.header_font_size)
            self.body_footer_font_size = int(self.header_font_size * 1)
            self.msg_font = ImageFont.truetype(self.font_family, self.body_footer_font_size)
            self.footer_font = ImageFont.truetype(self.font_family, self.body_footer_font_size - 5)
        except Exception as e:
            log.error(f"Failed to load font {self.font_family}: {e}")
            # Fallback to default font if necessary
            self.header_font = ImageFont.load_default()
            self.msg_font = ImageFont.load_default()
            self.footer_font = ImageFont.load_default()

        self.font_color = (249, 204, 115)

    def update_pos_and_font(self, next_font, text, draw, cur_pos, cur_font, img_size):
        W, H = img_size
        
        # Calculate text size (handling different Pillow versions)
        try:
            # For older Pillow
            prev_size = draw.textsize(text, font=cur_font)
        except AttributeError:
            # For newer Pillow
            left, top, right, bottom = draw.textbbox((0, 0), text, font=cur_font)
            prev_size = (right - left, bottom - top)

        cur_w, cur_h = cur_pos
        cur_h = cur_pos[1] + prev_size[1]

        # body indentation logic from original script
        if cur_font == self.header_font:
            cur_h += H // 68

        # footer right alignment logic from original script
        if next_font == self.footer_font and cur_font != self.footer_font:
            cur_h = H - 160

        # update font and position
        cur_pos = (cur_w, cur_h + self.line_separation)
        draw.text(cur_pos, text, font=next_font, fill=self.font_color)
        return cur_pos, next_font

    def gen_img(self, remark_name: str) -> str:
        # Load the background image
        bg_path = "./imgs/2024_traditional.jpg"
        if not os.path.exists(bg_path):
            log.warning(f"Background image {bg_path} not found. Creating a blank one.")
            img = Image.new('RGB', (800, 1200), color=(255, 0, 0)) # Red background as fallback
        else:
            img = Image.open(bg_path)
        
        W, H = img.size
        
        header = f"祝{remark_name}:"
        msg = "龙腾四海，"
        msg2 = "瑞气盈门!"
        footer  = "      Zack in Philly"
        footer2 = "     zackLight.com"

        draw = ImageDraw.Draw(img)
        cur_pos = (270, 20)
        cur_font = self.header_font
        
        draw.text(cur_pos, header, font=cur_font, fill=self.font_color)

        cur_pos, cur_font = self.update_pos_and_font(self.msg_font, msg, draw, cur_pos, cur_font, (W, H))
        cur_pos, cur_font = self.update_pos_and_font(self.msg_font, msg2, draw, cur_pos, cur_font, (W, H))
        cur_pos, cur_font = self.update_pos_and_font(self.footer_font, footer, draw, cur_pos, cur_font, (W, H))
        cur_pos, cur_font = self.update_pos_and_font(self.footer_font, footer2, draw, cur_pos, cur_font, (W, H))

        file_path = f"cards/{remark_name}.png"
        img.save(file_path)
        log.info(f"Generated image for {remark_name} at {file_path}")
        return file_path

class LunarNewYearBot(Wechaty):
    def __init__(self):
        super().__init__()
        self.generator = ImageGenerator()
        self.progress_file = 'progress.json'
        self.progress = self.load_progress()
        self.skip_list = ["Zack Light", "佳恒", "晨瑜"]
        self.divider = "皓怡"
        self.is_sending = False

    def load_progress(self) -> Dict[str, bool]:
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                log.error(f"Failed to load progress: {e}")
        return {}

    def save_progress(self):
        try:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(self.progress, f, ensure_ascii=False, indent=2)
        except Exception as e:
            log.error(f"Failed to save progress: {e}")

    async def on_scan(self, status: ScanStatus, qr_code: str = None, data: str = None):
        if qr_code:
            log.info(f"Scan QR Code to login ({status}): {qr_code}")
            qrcode_terminal.draw(qr_code)

    async def on_login(self, contact: Contact):
        log.info(f'User {contact} logged in')
        if not self.is_sending:
            self.is_sending = True
            asyncio.create_task(self.send_wishes())

    async def send_wishes(self):
        log.info('Starting to send wishes...')
        
        # Wait a bit for the bot to sync contacts
        await asyncio.sleep(5)
        
        all_contacts: List[Contact] = await self.Contact.find_all()
        log.info(f'Found {len(all_contacts)} contacts. Fetching names and sorting...')
        
        # To maintain the divider logic, we sort contacts by their display name
        contacts_with_names = []
        for contact in all_contacts:
            if contact.type() != Contact.Type.Individual or contact.is_self():
                continue
            name = await contact.alias() or await contact.name()
            if name:
                contacts_with_names.append((name, contact))
        
        # Sort alphabetically
        contacts_with_names.sort(key=lambda x: x[0])
        log.info(f'Processing {len(contacts_with_names)} individual contacts after sorting.')
        
        post_mode = False
        
        for name, contact in contacts_with_names:
            if name == self.divider:
                log.info(f"Reached divider: {name}. Switching to post mode.")
                post_mode = True
                
            if name in self.skip_list:
                log.debug(f"Skipping {name} (in skip list)")
                continue
                
            if self.progress.get(name):
                log.debug(f"Skipping {name} (already done)")
                continue
            
            log.info(f'Processing {name} (Mode: {"POST" if post_mode else "SHORT"})...')
            
            try:
                if post_mode:
                    wish = (f'祝{name}2024年龙腾万里，福禄双全! '
                            f'我去年跳槽到到费城一家做高频交易的公司了,学到了很多新知识也认识了很多新朋友~ '
                            f'感谢过去一年里您的帮助!\n\nzackLight.com')
                    await contact.say(wish)
                    
                    img_path = self.generator.gen_img(name)
                    file_box = FileBox.from_file(img_path)
                    await contact.say(file_box)
                    await asyncio.sleep(3) # Throttle to avoid being flagged
                else:
                    wish = '我去年跳槽到到费城一家做高频交易的公司了,学到了很多新知识也认识了很多新朋友~'
                    await contact.say(wish)
                    await asyncio.sleep(1.5)

                self.progress[name] = True
                self.save_progress()
            except Exception as e:
                log.error(f'Failed to send to {name}: {e}')
                await asyncio.sleep(5) # Wait longer on error
        
        log.info('All wishes processed!')
        self.is_sending = False

async def main():
    bot = LunarNewYearBot()
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())
