import os
from PIL import Image, ImageDraw, ImageFont

class CardNewsGenerator:
    """
    3D 배경 이미지와 선명한 한글 타이포그래피(Pillow)를 자동 합성하는 카드뉴스 생성기
    - 슬라이드 위치(처음/중간/마지막)에 따라 하단 안내문구(CTA) 자동 조절
    """
    FONT_PATH = 'C:/Windows/Fonts/malgunbd.ttf'

    @classmethod
    def wrap_text(cls, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> str:
        lines = []
        for line in text.split('\n'):
            words = line.split(' ')
            current_line = []
            for word in words:
                test_line = ' '.join(current_line + [word])
                bbox = font.getbbox(test_line)
                w = bbox[2] - bbox[0]
                if w <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        lines.append(word)
                        current_line = []
            if current_line:
                lines.append(' '.join(current_line))
        return '\n'.join(lines)

    @classmethod
    def generate_carousel_slides(cls, slides_data: list, output_dir: str) -> list:
        os.makedirs(output_dir, exist_ok=True)
        total_slides = len(slides_data)
        generated_paths = []

        font_title = ImageFont.truetype(cls.FONT_PATH, 50)
        font_sub = ImageFont.truetype(cls.FONT_PATH, 30)
        font_badge = ImageFont.truetype(cls.FONT_PATH, 26)

        for idx, s in enumerate(slides_data, start=1):
            is_last = (idx == total_slides)
            
            base_dir = os.path.dirname(__file__)
            bg_path = s.get('bg_path') or os.path.join(base_dir, 'default_card_news.png')
            
            img = Image.open(bg_path).convert('RGBA')
            width, height = img.size
            
            overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            
            card_x1, card_y1 = 60, height // 5
            card_x2, card_y2 = width - 60, height - 120
            max_text_width = (card_x2 - card_x1) - 80
            
            # 다크 네이비 / 글래스 패널
            draw.rounded_rectangle(
                [card_x1, card_y1, card_x2, card_y2],
                radius=32,
                fill=(15, 23, 42, 225),
                outline=(255, 255, 255, 60),
                width=3
            )
            
            # 뱃지 (Badge)
            badge_text = s.get('badge', f'1분 손해방지 꿀팁 STEP {idx:02d}')
            draw.rounded_rectangle(
                [card_x1 + 40, card_y1 + 40, card_x1 + 480, card_y1 + 100],
                radius=16,
                fill=(193, 53, 132, 240)
            )
            draw.text((card_x1 + 60, card_y1 + 53), badge_text, font=font_badge, fill=(255, 255, 255))
            
            # 제목 (Title)
            raw_title = s.get('title', '')
            wrapped_title = cls.wrap_text(raw_title, font_title, max_text_width)
            draw.text((card_x1 + 40, card_y1 + 130), wrapped_title, font=font_title, fill=(255, 255, 255), spacing=12)
            
            # 내용 (Description)
            raw_desc = s.get('desc', '')
            wrapped_desc = cls.wrap_text(raw_desc, font_sub, max_text_width)
            draw.text((card_x1 + 40, card_y1 + 310), wrapped_desc, font=font_sub, fill=(226, 232, 240), spacing=16)
            
            # 하단 CTA
            if is_last:
                footer_text = '💡 유용한 꿀팁! 지금 [저장(Bookmark)] & [공유] 해두세요!'
                footer_color = (74, 222, 128)
            else:
                footer_text = '▶️ 옆으로 넘겨서 다음 꿀팁 보기'
                footer_color = (56, 189, 248)

            draw.text((card_x1 + 40, card_y2 - 70), footer_text, font=font_badge, fill=footer_color)
            
            final_img = Image.alpha_composite(img, overlay)
            out_filename = os.path.join(output_dir, f'carousel_slide_{idx}.png')
            final_img.convert('RGB').save(out_filename)
            generated_paths.append(out_filename)

        return generated_paths

if __name__ == '__main__':
    print("CardNewsGenerator module initialized.")
