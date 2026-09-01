import os
import sys
import urllib.request
import xml.etree.ElementTree as ET

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from card_news_generator import CardNewsGenerator
from gemini_content_engine import GeminiContentEngine

def fetch_latest_news(limit=15):
    """구글 뉴스 한국 RSS에서 최신 헤드라인을 가져옵니다."""
    url = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"
    headlines = []
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            for item in root.findall('./channel/item'):
                title = item.find('title').text
                pub_date = item.find('pubDate')
                date_str = pub_date.text if pub_date is not None else ""
                
                # 구글 뉴스는 주로 "제목 - 언론사" 형태를 띕니다.
                headlines.append(f"{title} / 발행일: {date_str}")
                if len(headlines) >= limit:
                    break
    except Exception as e:
        print(f"[RSS Fetch Error] {e}")
    return headlines

def main():
    print("📰 구글 뉴스 최신 헤드라인을 가져오는 중...")
    headlines = fetch_latest_news()
    if not headlines:
        print("❌ 뉴스를 가져오지 못했습니다.")
        return

    print("🤖 Gemini AI로 '손해방지' 컨셉 뉴스 선정 및 슬라이드 생성 중...")
    engine = GeminiContentEngine()
    result = engine.generate_news_slides_from_headlines(headlines)
    
    if not result or "slides" not in result or "caption" not in result:
        print("❌ 데이터 생성에 실패했습니다.")
        return

    slides_data = result["slides"]
    caption = result["caption"]
    json_data = result
    news_source = result.get("source")
    news_date = result.get("date")

    if len(slides_data) != 5:
        print("❌ 슬라이드 데이터가 5장이 아닙니다.")
        return

    print("🎨 카드뉴스 렌더링 시작...")
    out_dir = os.path.join(os.path.dirname(__file__), "generated_slides", "daily_news")
    generated_slides = CardNewsGenerator.generate_carousel_slides(slides_data, out_dir)
    
    # 인스타그램 캡션 및 스레드 포스트 저장
    caption = json_data.get("caption", "")
    threads_post = json_data.get("threads_post", "")

    if news_source and news_date:
        prefix = f"[출처: {news_source} | 발행일: {news_date}]\n\n"
        caption = prefix + caption
        threads_post = prefix + threads_post

    caption_path = os.path.join(out_dir, "caption.txt")
    with open(caption_path, "w", encoding="utf-8") as f:
        f.write(caption)

    threads_path = os.path.join(out_dir, "threads.txt")
    with open(threads_path, "w", encoding="utf-8") as f:
        f.write(threads_post)

    print(f"✅ 일일 최신 뉴스 카드뉴스, 캡션, 스레드 글 생성 완료! 저장 위치: {out_dir}")
    for slide in generated_slides:
        print(slide)

    print("\n---------------------------------------------------------")
    print("📢 [승인 대기] 콘텐츠가 성공적으로 생성되었습니다.")
    print("생성된 이미지와 캡션을 확인하신 후, 업로드를 원하시면")
    print("채팅창에 '업로드 진행해'라고 말씀해 주시거나, ")
    print("별도의 업로드 스크립트(upload_daily_news.py)를 실행해 주세요!")
    print("---------------------------------------------------------")

if __name__ == "__main__":
    main()
