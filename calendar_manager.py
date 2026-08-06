import json
import os
from datetime import datetime, timedelta

CALENDAR_FILE = os.path.join(os.path.dirname(__file__), 'calendar_posts.json')

class CalendarManager:
    """
    30일간 하루 4회(오전 2회, 오후 2회) 인스타그램 포스팅 캘린더 데이터베이스 관리 클래스
    """
    SLOTS = [
        {"id": "morning_1", "time": "07:30", "name": "오전 1차 (출근길 피크)"},
        {"id": "morning_2", "time": "11:45", "name": "오전 2차 (점심 전 피크)"},
        {"id": "afternoon_1", "time": "17:30", "name": "오후 1차 (퇴근길 피크)"},
        {"id": "afternoon_2", "time": "21:15", "name": "오후 2차 (야간 골든타임)"}
    ]

    def __init__(self):
        self.calendar_file = CALENDAR_FILE
        self._ensure_calendar_exists()

    def _ensure_calendar_exists(self):
        if not os.path.exists(self.calendar_file):
            self.generate_30day_schedule()

    def generate_30day_schedule(self, days: int = 365):
        """
        오늘부터 지정한 일수(기본 365일, 1년) 동안의 하루 4회 포스팅 슬롯 캘린더 생성
        """
        today = datetime.now().date()
        schedule_data = []

        for day_offset in range(days):
            target_date = today + timedelta(days=day_offset)
            date_str = target_date.strftime("%Y-%m-%d")

            for slot in self.SLOTS:
                item = {
                    "id": f"{date_str}_{slot['id']}",
                    "date": date_str,
                    "slot_id": slot['id'],
                    "slot_time": slot['time'],
                    "slot_name": slot['name'],
                    "status": "SCHEDULED", # SCHEDULED, PUBLISHED, FAILED
                    "topic": "",
                    "caption": "",
                    "media_url": "",
                    "media_id": "",
                    "published_at": ""
                }
                schedule_data.append(item)

        with open(self.calendar_file, "w", encoding="utf-8") as f:
            json.dump(schedule_data, f, ensure_ascii=False, indent=2)

        return schedule_data

    def get_all_posts(self):
        if not os.path.exists(self.calendar_file):
            return self.generate_30day_schedule()
        with open(self.calendar_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_post_by_id(self, post_id: str):
        posts = self.get_all_posts()
        for p in posts:
            if p["id"] == post_id:
                return p
        return None

    def update_post_status(self, post_id: str, status: str, topic: str = "", caption: str = "", media_url: str = "", media_id: str = ""):
        posts = self.get_all_posts()
        updated = False

        for p in posts:
            if p["id"] == post_id:
                p["status"] = status
                if topic: p["topic"] = topic
                if caption: p["caption"] = caption
                if media_url: p["media_url"] = media_url
                if media_id: p["media_id"] = media_id
                if status == "PUBLISHED":
                    p["published_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                updated = True
                break

        if updated:
            with open(self.calendar_file, "w", encoding="utf-8") as f:
                json.dump(posts, f, ensure_ascii=False, indent=2)
        return updated

if __name__ == "__main__":
    cm = CalendarManager()
    print("30일 포스팅 캘린더 슬롯 개수:", len(cm.get_all_posts()))
