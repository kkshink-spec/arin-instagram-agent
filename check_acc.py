import requests

token = "IGAAO3WRMmXXFBZAFlkZA0ZA4cGpiOWYyZAlpBOWJEY0wzS1gyWE54N1RiNnlNQlhhdWg5RktFS1k5bGI3M1YwbXh2ZAFJGa2tfQk1ma3RqVTZAYOWRjVDlSd01pZAEdTUC1ldzdOV19tUTBxOVY4UU9zNmFQdDB3"
acc_id = "27646020745040681"

# 직접 계정 정보 조회
url = f"https://graph.facebook.com/v23.0/{acc_id}?fields=id,username,name&access_token={token}"
res = requests.get(url).json()

print("Direct ID Lookup Result:")
print(res)
