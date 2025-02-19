import yt_dlp

# 設定 YouTube 頻道的 URL
channel_url = 'https://www.youtube.com/@games002-n3u/videos'

# 設定輸出文字檔的路徑
output_file = 'long_videos.txt'

# 設定 yt-dlp 的選項
ydl_opts = {
   'quiet': True,  # 靜默模式，不顯示下載進度
   'extract_flat': True,  # 僅提取影片資訊，不下載影片
}

# 使用 yt-dlp 抓取頻道影片資訊
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
   result = ydl.extract_info(channel_url, download=False)
   if 'entries' in result:
       # 過濾出 20 分鐘以上的影片
       long_videos = [
           (entry['title'], entry['url'])
           for entry in result['entries']
           if entry.get('duration', 0) >= 1200  # 1200 秒等於 20 分鐘
       ]

# 將結果寫入文字檔
with open(output_file, 'w', encoding='utf-8') as f:
   for title, url in long_videos:
       f.write(f'{title} {url}\n')

print(f'已將 20 分鐘以上的影片資訊寫入 {output_file}')
