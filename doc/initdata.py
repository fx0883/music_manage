import requests
import json

# API URL
url = 'http://35.188.0.156:8000/music/soundcloud/search/'

# CSRF Token
csrf_token = 'N2ZW8YjTvr4wnFuOklio2OUoF9VoMzUA9c7mf7rzPV0C4mc73xADdaIbbXi4Rd13'

# Title 列表
titles = [
    "Hip Hop & Rap", "Electronic", "Pop", "R&B", "Chill",
    "Party", "Workout", "Techno", "House", "Feel Good", "At home"
]

# Headers
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'X-CSRFTOKEN': csrf_token
}

# 遍历每个 title 并调用 API
for title in titles:
    # POST 请求数据
    data = {
        "q": title,
        "limit": 1200,
        "offset": 1
    }

    # 发送 POST 请求
    response = requests.post(url, headers=headers, data=json.dumps(data))



    # 打印结果
    if response.status_code == 200:
        print(f"Search for '{title}' completed. Response: {len(response.json())}")

    else:
        print(f"Failed to search for '{title}'. Status code: {response.status_code}")

