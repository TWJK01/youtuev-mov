from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

def get_long_videos(channel_url):
    options = Options()
    options.add_argument("--headless")  # 無頭模式，不開啟瀏覽器視窗
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(channel_url)
    time.sleep(5)  # 等待頁面加載

    videos = []
    video_elements = driver.find_elements(By.XPATH, '//a[@id="video-title"]')

    for video in video_elements:
        title = video.get_attribute("title")
        url = video.get_attribute("href")
        
        # 找到對應的時間標籤
        try:
            duration_element = video.find_element(By.XPATH, './/ancestor::ytd-thumbnail//ytd-thumbnail-overlay-time-status-renderer//span')
            duration_text = duration_element.text.strip()
            match = re.match(r"(\d+):(\d+)", duration_text)
            if match:
                minutes = int(match.group(1))
                seconds = int(match.group(2))
                if minutes >= 20:
                    videos.append(f"{title}, {url}")
        except:
            pass  # 如果找不到時間，跳過

    driver.quit()
    return videos

def save_to_file(video_list, filename="videos_list.txt"):
    if not video_list:
        video_list.append("No videos found")

    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(video_list))
    print(f"Saved {len(video_list)} videos to {filename}")

if __name__ == "__main__":
    channel_url = "https://www.youtube.com/@tagtheatre1475/videos"
    videos = get_long_videos(channel_url)
    save_to_file(videos)
