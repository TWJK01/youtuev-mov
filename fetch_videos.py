import yt_dlp

# 设置 YouTube 频道 URL
channel_url = 'https://www.youtube.com/@games002-n3u/videos'

# 设置 yt-dlp 的选项
ydl_opts = {
    'quiet': True,        # 静默模式
    'extract_flat': True, # 仅提取视频信息，不下载视频
}

# 使用 yt-dlp 抓取视频信息
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    result = ydl.extract_info(channel_url, download=False)
    videos = result.get('entries', [])

# 过滤出时长超过 20 分钟（1200 秒）的视频
long_videos = []
for video in videos:
    # 获取每个视频的详细信息
    video_info = ydl.extract_info(video['url'], download=False)
    duration = video_info.get('duration', 0)
    if duration > 1200:
        long_videos.append({
            'title': video_info.get('title', '无标题'),
            'url': video_info.get('webpage_url', '无网址')
        })

# 将视频标题和网址以「标题,网址」格式写入文本文件
with open('long_videos.txt', 'w', encoding='utf-8') as f:
    for video in long_videos:
        f.write(f"{video['title']},{video['url']}\n")

print(f'已将 {len(long_videos)} 部视频信息写入 long_videos.txt')
