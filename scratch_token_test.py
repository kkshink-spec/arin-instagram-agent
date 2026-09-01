import requests
import json
import datetime

token = "EAAQcbg84GnABSczDn8MOxEZBZBxuYbfLaVGonVSburg6SZCa92uF2ZClBhZAGPsX7xjmcctzaDTQ5ToiuVUNktrPLq3zddUaWmGlvxZC44vxDRyuE9PcyPvDZCn33U3mGxgzTh75vG4xIpYI3Fhal36nsvq0Xvl8SV8c4AjrOPTZAzHHU9ouDA2rRwa75HLI7iJ3"
url = f"https://graph.facebook.com/v20.0/debug_token?input_token={token}&access_token={token}"
res = requests.get(url).json()

print(json.dumps(res, indent=2))
if 'data' in res and 'expires_at' in res['data']:
    expires = res['data']['expires_at']
    if expires == 0:
        print("Expires: Never (0)")
    else:
        print("Expires:", datetime.datetime.fromtimestamp(expires))
