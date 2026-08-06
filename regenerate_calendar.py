import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from calendar_manager import CalendarManager

if __name__ == "__main__":
    cm = CalendarManager()
    posts = cm.generate_30day_schedule()
    print(f"🎉 30일(총 {len(posts)}개 슬롯) '손해를 막아주는 정보' 테마 캘린더 DB 재구성 완료!")
