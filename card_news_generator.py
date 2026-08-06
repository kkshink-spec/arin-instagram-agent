import os
from PIL import Image, ImageDraw, ImageFont

class CardNewsGenerator:
    """
    3D 배경 이미지와 선명한 한글 타이포그래피(Pillow)를 자동 합성하는 카드뉴스 생성기
    - 슬라이드 위치(처음/중간/마지막)에 따라 하단 안내문구(CTA) 자동 조절
    """
    FONT_PATH = 'C:/Windows/Fonts/malgunbd.ttf'

    @classmethod
    def generate_carousel_slides(cls, slides_data: list, output_dir: str) -> list:
        """
        slides_data: [
            {'title': '...', 'desc': '...', 'badge': '...'},
            ...
        ]
        """
        os.makedirs(output_dir, exist_ok=True)
        total_slides = len(slides_data)
        generated_paths = []

        font_title = ImageFont.truetype(cls.FONT_PATH, 56)
        font_sub = ImageFont.truetype(cls.FONT_PATH, 34)
        font_badge = ImageFont.truetype(cls.FONT_PATH, 28)

        for idx, s in enumerate(slides_data, start=1):
            is_last = (idx == total_slides)
            
            # 배경 이미지 (기본 고화질 3D 글래스모피즘 이미지)
            base_dir = os.path.dirname(__file__)
            bg_path = s.get('bg_path') or os.path.join(base_dir, 'default_card_news.png')
            
            img = Image.open(bg_path).convert('RGBA')
            width, height = img.size
            
            # 반투명 다크 패널 생성
            overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            
            card_x1, card_y1 = 80, height // 4
            card_x2, card_y2 = width - 80, height - 180
            
            draw.rounded_rectangle(
                [card_x1, card_y1, card_x2, card_y2],
                radius=30,
                fill=(15, 23, 42, 215),
                outline=(255, 255, 255, 45),
                width=2
            )
            
            # 뱃지 (Badge)
            badge_text = s.get('badge', f'SLIDE {idx:02d}')
            draw.rounded_rectangle(
                [card_x1 + 40, card_y1 + 40, card_x1 + 380, card_y1 + 100],
                radius=15,
                fill=(193, 53, 132, 230)
            )
            draw.text((card_x1 + 60, card_y1 + 52), badge_text, font=font_badge, fill=(255, 255, 255))
            
            # 제목 (Title)
            title_text = s.get('title', '')
            draw.text((card_x1 + 40, card_y1 + 140), title_text, font=font_title, fill=(255, 255, 255), spacing=15)
            
            # 내용 (Description)
            desc_text = s.get('desc', '')
            draw.text((card_x1 + 40, card_y1 + 320), desc_text, font=font_sub, fill=(226, 232, 240), spacing=20)
            
            # 하단 안내문구 (마지막 슬라이드인 경우 더보기 대신 저장/공유 유도)
            if is_last:
                footer_text = '💡 도움이 되셨다면 [저장(Bookmark)] & [공유] 클릭!'
                footer_color = (74, 222, 128) # 밝은 에메랄드 그린
            else:
                footer_text = '▶️ 다음 슬라이드로 넘겨서 더보기'
                footer_color = (56, 189, 248) # 밝은 스카이 블루

            draw.text((card_x1 + 40, card_y2 - 70), footer_text, font=font_badge, fill=footer_color)
            
            final_img = Image.alpha_composite(img, overlay)
            out_filename = os.path.join(output_dir, f'carousel_slide_{idx}.png')
            final_img.convert('RGB').save(out_filename)
            generated_paths.append(out_filename)

        return generated_paths

if __name__ == '__main__':
    print("CardNewsGenerator module initialized.")
