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

        font_title = ImageFont.truetype(cls.FONT_PATH, 55)
        font_sub = ImageFont.truetype(cls.FONT_PATH, 45)
        font_badge = ImageFont.truetype(cls.FONT_PATH, 34)

        for idx, s in enumerate(slides_data, start=1):
            is_last = (idx == total_slides)
            
            default_bg_path = os.path.join(os.path.dirname(__file__), 'custom_bg.jpg')
            if s.get('bg_path') and os.path.exists(s.get('bg_path')):
                img = Image.open(s.get('bg_path')).convert('RGBA')
                width, height = img.size
            elif os.path.exists(default_bg_path):
                # 생성한 미니멀 & 모던 기본 배경 사용
                img = Image.open(default_bg_path).convert('RGBA')
                img = img.resize((1080, 1080), Image.Resampling.LANCZOS)
                width, height = img.size
            else:
                # 고정된 배경 이미지 대신 1080x1080 그라데이션 배경 동적 생성
                width, height = 1080, 1080
                img = Image.new('RGBA', (width, height))
                draw_bg = ImageDraw.Draw(img)
                # 약간씩 다른 색상을 위해 슬라이드 인덱스(idx) 활용
                base_r, base_g, base_b = (10 + idx*5) % 40, (15 + idx*10) % 50, (30 + idx*15) % 80
                for i in range(height):
                    r = int(base_r - (base_r * (i / height)))
                    g = int(base_g - (base_g * (i / height)))
                    b = int(base_b - (base_b * (i / height)))
                    draw_bg.line([(0, i), (width, i)], fill=(r, g, b, 255))

            
            overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            
            card_x1, card_y1 = 50, 120
            card_x2, card_y2 = width - 50, height - 80
            max_text_width = (card_x2 - card_x1) - 80
            
            # 네모 박스 배경을 바탕과 동일하게(투명) 처리
            draw.rounded_rectangle(
                [card_x1, card_y1, card_x2, card_y2],
                radius=32,
                fill=(0, 0, 0, 0),
                outline=(0, 0, 0, 30),
                width=3
            )
            
            # 뱃지 (Badge)
            badge_text = s.get('badge', f'손해방지 꿀팁 STEP {idx:02d}').replace('1분 ', '')
            draw.text((card_x1 + 40, card_y1 + 55), badge_text, font=font_badge, fill=(0, 0, 0))
            
            # 제목 (Title)
            raw_title = s.get('title', '')
            wrapped_title = cls.wrap_text(raw_title, font_title, max_text_width)
            draw.multiline_text((card_x1 + 40, card_y1 + 140), wrapped_title, font=font_title, fill=(0, 0, 0), spacing=20)
            
            # 제목의 높이를 계산하여 내용(Description) Y좌표 결정
            title_bbox = draw.multiline_textbbox((card_x1 + 40, card_y1 + 140), wrapped_title, font=font_title, spacing=20)
            print(f"Slide {idx} title_bbox:", title_bbox, "wrapped_title lines:", len(wrapped_title.split('\n')))
            desc_start_y = title_bbox[3] + 60 # 제목 아래 60px 간격 추가
            
            # 내용 (Description)
            raw_desc = s.get('desc', '')
            wrapped_desc = cls.wrap_text(raw_desc, font_sub, max_text_width)
            draw.multiline_text((card_x1 + 40, desc_start_y), wrapped_desc, font=font_sub, fill=(0, 0, 0), spacing=24)
            
            # 하단 CTA
            if is_last:
                footer_text = '유용한 꿀팁! 지금 [저장(Bookmark)] & [공유] 해두세요!'
                footer_color = (0, 0, 0)
            else:
                if idx == 1:
                    footer_text = '옆으로 넘겨서 꿀팁 확인하기 >'
                else:
                    footer_text = '옆으로 넘겨서 다음 꿀팁 보기 >'
                footer_color = (0, 0, 0)

            draw.text((card_x1 + 40, card_y2 - 70), footer_text, font=font_badge, fill=footer_color)
            
            final_img = Image.alpha_composite(img, overlay)
            out_filename = os.path.join(output_dir, f'carousel_slide_{idx}.png')
            final_img.convert('RGB').save(out_filename)
            generated_paths.append(out_filename)

        return generated_paths

if __name__ == '__main__':
    print("CardNewsGenerator module initialized.")
