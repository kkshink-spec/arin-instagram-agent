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

class AutoInstagramScheduler:
    """
    1개월간 하루 4회(07:30, 11:45, 17:30, 21:15) 자동 포스팅 및 캘린더 관리 스케줄러
    """
    def __init__(self):
        self.cm = CalendarManager()
        self.account_id = os.getenv("INSTAGRAM_ACCOUNT_ID", "27646020745040681")
        self.access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN", "IGAAO3WRMmXXFBZAFlkZA0ZA4cGpiOWYyZAlpBOWJEY0wzS1gyWE54N1RiNnlNQlhhdWg5RktFS1k5bGI3M1YwbXh2ZAFJGa2tfQk1ma3RqVTZAYOWRjVDlSd01pZAEdTUC1ldzdOV19tUTBxOVY4UU9zNmFQdDB3")
        self.uploader = InstaUploader(self.account_id, self.access_token, verbose=False)

    def execute_post_for_slot(self, post_item: dict):
        post_id = post_item["id"]
        slot_id = post_item["slot_id"]
        
        print(f"[Scheduler] Executing scheduled post: {post_id} ({post_item['slot_name']})")
        
        # 1. 트렌드 및 프롬프트/캡션 수집
        trend_data = TrendAnalyzer.get_trend_for_slot(slot_id)
        topic = trend_data["topic"]
        caption = trend_data["caption"]
        
        # 2. 이미지 준비 (미리 준비된 바이럴 이미지 또는 기본 고화질 이미지 사용)
        base_dir = os.path.dirname(__file__)
        fallback_img = os.path.join(base_dir, "default_card_news.png")

        # 3. 인스타그램 업로드
        result = self.uploader.upload_image(fallback_img, caption)
        
        if result and "id" in result:
            media_id = result["id"]
            self.cm.update_post_status(
                post_id=post_id,
                status="PUBLISHED",
                topic=topic,
                caption=caption,
                media_url=fallback_img,
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
        현재 시각과 캘린더 슬롯을 비교하여 정해진 시간에 포스팅 실행
        """
        now = datetime.now()
        current_date_str = now.strftime("%Y-%m-%d")
        current_time_str = now.strftime("%H:%M")
        
        all_posts = self.cm.get_all_posts()
        
        for p in all_posts:
            if p["date"] == current_date_str and p["status"] == "SCHEDULED":
                # 현재 시각이 슬롯 타임과 같거나 지난 경우 (미이행 슬롯) 실행
                if current_time_str >= p["slot_time"]:
                    self.execute_post_for_slot(p)

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
