import time
import os
import sys
from datetime import datetime, timezone, timedelta
from calendar_manager import CalendarManager
from trend_analyzer import TrendAnalyzer
from insta_uploader import InstaUploader
from image_hoster import LocalMediaHoster

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from card_news_generator import CardNewsGenerator

KST = timezone(timedelta(hours=9))

class AutoInstagramScheduler:
    """
    1개월간 하루 5회(07:30, 08:00, 11:30, 17:30, 18:00) 자동 포스팅 및 캘린더 관리 스케줄러 (KST 표준시 준수)
    """
    def __init__(self):
        self.cm = CalendarManager()
        self.account_id = os.getenv("INSTAGRAM_ACCOUNT_ID", "27646020745040681")
        self.access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN", "IGAAO3WRMmXXFBZAFlkZA0ZA4cGpiOWYyZAlpBOWJEY0wzS1gyWE54N1RiNnlNQlhhdWg5RktFS1k5bGI3M1YwbXh2ZAFJGa2tfQk1ma3RqVTZAYOWRjVDlSd01pZAEdTUC1ldzdOV19tUTBxOVY4UU9zNmFQdDB3")
        self.uploader = InstaUploader(self.account_id, self.access_token, verbose=True)

    def execute_post_for_slot(self, post_item: dict):
        post_id = post_item["id"]
        slot_id = post_item["slot_id"]
        
        print(f"[Scheduler] Executing scheduled post: {post_id} ({post_item['slot_name']})")
        
        # 1. 트렌드 데이터 및 슬라이드 구성요소 수집
        trend_data = TrendAnalyzer.get_trend_for_slot(slot_id)
        topic = trend_data["topic"]
        slides_data = trend_data["slides"]
        caption = trend_data["caption"]
        
        # 2. CardNewsGenerator로 한글 타이포그래피 카드뉴스 이미지(캐러셀 슬라이드) 렌더링
        base_dir = os.path.dirname(__file__)
        output_dir = os.path.join(base_dir, "generated_slides", f"post_{post_id}")
        generated_slides = CardNewsGenerator.generate_carousel_slides(slides_data, output_dir)
        print(f"[Scheduler] {len(generated_slides)}개의 한글 카드뉴스 슬라이드가 성공적으로 생성되었습니다: {generated_slides}")

        # 3. 인스타그램 캐러셀 업로드
        result = self.uploader.upload_carousel(generated_slides, caption)
        
        if result and "id" in result:
            media_id = result["id"]
            self.cm.update_post_status(
                post_id=post_id,
                status="PUBLISHED",
                topic=topic,
                caption=caption,
                media_url=generated_slides[0],
                media_id=media_id
            )
            print(f"[Scheduler Success] Published post ID {post_id} -> Instagram Media ID: {media_id}")
            return True
        else:
            self.cm.update_post_status(
                post_id=post_id,
                status="FAILED",
                topic=topic,
                caption=caption
            )
            print(f"[Scheduler Error] Failed to publish post ID {post_id}: {result}")
            return False

    def run_check_cycle(self):
        """
        KST(한국 표준시) 기준으로 현재 시각과 캘린더 슬롯을 비교하여 해당 시각 슬롯 1개만 안전하게 실행
        """
        now = datetime.now(KST)
        current_date_str = now.strftime("%Y-%m-%d")
        current_time_str = now.strftime("%H:%M")
        
        print(f"[Scheduler Check] Current KST Time: {current_date_str} {current_time_str}")
        
        all_posts = self.cm.get_all_posts()
        
        # 오늘 날짜 예정된 포스트 추출
        today_scheduled = [
            p for p in all_posts 
            if p["date"] == current_date_str and p["status"] == "SCHEDULED"
        ]
        
        # 현재 시각 이하(도달한 시간대) 중 가장 최근 시각 슬롯 1개 선택
        eligible = [p for p in today_scheduled if current_time_str >= p["slot_time"]]
        
        if eligible:
            # 가장 시각 차이가 적은(가장 최근) 슬롯 1개 선택
            target_post = max(eligible, key=lambda x: x["slot_time"])
            print(f"[Scheduler] Target slot found: {target_post['id']} ({target_post['slot_name']} @ {target_post['slot_time']})")
            self.execute_post_for_slot(target_post)
        else:
            print("[Scheduler] No matching scheduled slot for the current time window.")

    def start_loop(self):
        print("🤖 [AutoInstagramScheduler] 30-Day Auto Instagram Scheduler Started (KST Mode)!")
        print("📅 Schedules: 07:30 | 08:00 | 11:30 | 17:30 | 18:00 (5 Posts Daily)")
        
        while True:
            try:
                self.run_check_cycle()
            except Exception as e:
                print(f"[Scheduler Exception]: {e}")
            time.sleep(45)

if __name__ == "__main__":
    scheduler = AutoInstagramScheduler()
    if "--once" in sys.argv:
        print("🤖 [AutoInstagramScheduler] Executing single check cycle (--once)...")
        scheduler.run_check_cycle()
    else:
        scheduler.start_loop()

