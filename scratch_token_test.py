import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
import requests
import json
import datetime

token = os.getenv("META_ACCESS_TOKEN") or os.getenv("INSTAGRAM_ACCESS_TOKEN")
url = f"https://graph.facebook.com/v20.0/debug_token?input_token={token}&access_token={token}"
res = requests.get(url).json()

print(json.dumps(res, indent=2))
if 'data' in res and 'expires_at' in res['data']:
    expires = res['data']['expires_at']
    if expires == 0:
        print("Expires: Never (0)")
    else:
        print("Expires:", datetime.datetime.fromtimestamp(expires))
