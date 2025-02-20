import requests
from bs4 import BeautifulSoup
import re
import os

def get_long_videos(channel_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(channel_url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch page")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    videos = []
    for video in soup.find_all("a", href=re.compile(r"/watch\?v=")):
        title = video.get_text(strip=True)
        url = "https://www.youtube.com" + video["href"]
        
        duration_tag = video.find_next("span", class_=re.compile("style-scope ytd-thumbnail-overlay-time-status-renderer"))
        if duration_tag:
            duration_text = duration_tag.get_text(strip=True)
            match = re.match(r"(\d+):?(\d+)?", duration_text)
            if match:
                minutes = int(match.group(1))
                seconds = int(match.group(2)) if match.group(2) else 0
                if minutes >= 20:
                    videos.append(f"{title}, {url}")
    
    return videos

def save_to_file(video_list, filename="videos_list.txt"):
    # 如果檔案不存在，先建立
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as file:
            file.write("")

    # 確保即使沒有影片，仍然建立檔案
    if not video_list:
        video_list.append("No videos found")

    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(video_list))
    print(f"Saved {len(video_list)} videos to {filename}")

if __name__ == "__main__":
    channel_url = "https://www.youtube.com/@tagtheatre1475/videos"
    videos = get_long_videos(channel_url)
    save_to_file(videos)
