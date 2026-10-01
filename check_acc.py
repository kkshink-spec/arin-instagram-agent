import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
import requests

token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
acc_id = "27646020745040681"

# 직접 계정 정보 조회
url = f"https://graph.facebook.com/v23.0/{acc_id}?fields=id,username,name&access_token={token}"
res = requests.get(url).json()

print("Direct ID Lookup Result:")
print(res)
