import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID")

def analyze_insights():
    # 1. Fetch recent media
    url = f"https://graph.facebook.com/v20.0/{ACCOUNT_ID}/media"
    params = {
        "fields": "id,caption,media_type,media_url,timestamp,like_count,comments_count,permalink",
        "access_token": ACCESS_TOKEN,
        "limit": 50
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'data' not in data:
        print("Error fetching media:", data)
        return
        
    media_list = data['data']
    print(f"총 {len(media_list)}개의 최근 게시글을 찾았습니다.\n")
    
    # 2. Sort by likes/comments since standard insights (reach/impressions) require a specific edge
    # Let's just sort by likes first as a basic proxy for "most viewed" (조회수 많은거)
    # If the user wants specific video views, we need to check media_type == 'VIDEO'
    
    sorted_media = sorted(media_list, key=lambda x: x.get('like_count', 0) + x.get('comments_count', 0), reverse=True)
    
    print("반응이 가장 좋았던 상위 5개 게시물\n")
    for i, media in enumerate(sorted_media[:5]):
        caption = media.get('caption', '내용 없음').replace('\n', ' ')
        if len(caption) > 30:
            caption = caption[:30] + "..."
            
        print(f"{i+1}위: {caption}")
        print(f"   좋아요: {media.get('like_count', 0)}개 | 댓글: {media.get('comments_count', 0)}개")
        print(f"   링크: {media.get('permalink')}")
        print("-" * 50)

if __name__ == "__main__":
    analyze_insights()
