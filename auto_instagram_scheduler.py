import time
import os
import sys
from datetime import datetime
from calendar_manager import CalendarManager
from trend_analyzer import TrendAnalyzer
from insta_uploader import InstaUploader
from image_hoster import LocalMediaHoster

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from card_news_generator import CardNewsGenerator

class AutoInstagramScheduler:
    """
    1개월간 하루 5회(07:30, 08:00, 11:30, 17:30, 18:00) 자동 포스팅 및 캘린더 관리 스케줄러
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

from datetime import datetime, timezone, timedelta

    def run_check_cycle(self):
        """
        현재 시각과 캘린더 슬롯을 비교하여 정해진 시간에 포스팅 실행 (KST 한국 표준시 기준)
        """
        kst = timezone(timedelta(hours=9))
        now = datetime.now(kst)
        current_date_str = now.strftime("%Y-%m-%d")
        current_time_str = now.strftime("%H:%M")
        
        print(f"[Scheduler] Checking cycle at KST {current_date_str} {current_time_str}")
        all_posts = self.cm.get_all_posts()
        
        for p in all_posts:
            if p["date"] == current_date_str and p["status"] == "SCHEDULED":
                # 현재 시각이 슬롯 타임과 같거나 지난 경우 (미이행 슬롯) 실행
                if current_time_str >= p["slot_time"]:
                    self.execute_post_for_slot(p)
                    # 깃허브 액션 등 일회성 조회의 경우 하나씩 연속 처리 또는 순차 수행
                    break

    def start_loop(self):
        print("🤖 [AutoInstagramScheduler] 30-Day Auto Instagram Scheduler Started!")
        print("📅 Schedules: 07:30 | 11:45 | 17:30 | 21:15 (4 Posts Daily)")
        
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
