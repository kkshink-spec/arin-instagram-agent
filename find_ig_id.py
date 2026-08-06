import requests

token = "IGAAO3WRMmXXFBZAFlSS3FNS1Jna1V4VHhhSk5DMDhVNTl4bjNqcHJrTGUyS1pWNTJlM3lpQjdDc2QtSUR5YVVza21tN01HRFBXVXh6NmdEamNfMlE4aFQya2sxX2JmWVV2cE8zTzJSSFpOTmxoNzJ5ZAHNDS2FBMXB6S3JMZAWdCNAZDZD"

print("[1] 연결된 페이스북 페이지 및 인스타그램 비즈니스 계정 탐색 중...")
url1 = f"https://graph.facebook.com/v23.0/me/accounts?fields=id,name,access_token,instagram_business_account{{id,username,name}}&access_token={token}"
res1 = requests.get(url1).json()
print("페이지 목록:", res1)

print("\n[2] 내 비즈니스 매니저(Business Manager) 계정 탐색 중...")
url2 = f"https://graph.facebook.com/v23.0/me/businesses?access_token={token}"
res2 = requests.get(url2).json()
print("비즈니스 목록:", res2)

print("\n[3] 내 권한 목록 확인 중...")
url3 = f"https://graph.facebook.com/v23.0/me/permissions?access_token={token}"
res3 = requests.get(url3).json()
print("부여된 권한:", res3)
