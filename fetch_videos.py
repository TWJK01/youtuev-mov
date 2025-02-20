import yt_dlp
import json

# 設定 YouTube 頻道 URL
channel_url = 'https://www.youtube.com/@VideolandMovie/videos'

# 設定 yt-dlp 的選項
ydl_opts = {
    'quiet': True,        # 靜默模式
    'extract_flat': True, # 僅提取影片資訊，不下載影片
}

# 使用 yt-dlp 抓取影片資訊
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    result = ydl.extract_info(channel_url, download=False)
    videos = result.get('entries', [])

# 過濾出長度超過 20 分鐘（1200 秒）的影片
long_videos = [video for video in videos if video.get('duration', 0) > 1200]

# 將影片標題與網址以「網頁標題,網址」格式寫入文字檔
with open('long_videos.txt', 'w', encoding='utf-8') as f:
    for video in long_videos:
        title = video.get('title', '無標題')
        url = video.get('url', '無網址')
        f.write(f'{title},{url}\n')

print(f'已將 {len(long_videos)} 部影片資訊寫入 long_videos.txt')
