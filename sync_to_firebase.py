import os
import requests
import json

# 配置
REPO = "E5alR9/list"
FIREBASE_URL = "https://e5alr9-default-rtdb.asia-southeast1.firebasedatabase.app/.json"

def sync():
    # 1. 抓取 GitHub 檔案列表
    github_api_url = f"https://api.github.com/repos/{REPO}/contents/"
    response = requests.get(github_api_url)
    
    if response.status_code == 200:
        files = response.json()
        song_list = []
        
        for item in files:
            # 只抓取 mp3 檔案
            if item["type"] == "file" and item["name"].lower().endswith(".mp3"):
                song_list.append({
                    "name": item["name"],
                    "download_url": item["download_url"]
                })
        
        # 2. 推送到 Firebase (覆蓋模式)
        firebase_response = requests.put(FIREBASE_URL, data=json.dumps(song_list))
        
        if firebase_response.status_code == 200:
            print(f"成功同步 {len(song_list)} 首歌到 Firebase！")
        else:
            print("Firebase 寫入失敗:", firebase_response.text)
    else:
        print("GitHub 抓取失敗:", response.text)

if __name__ == "__main__":
    sync()
