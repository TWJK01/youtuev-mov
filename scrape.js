const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  // 開啟 headless 瀏覽器
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  
  // 前往指定的頻道影片頁面
  await page.goto('https://www.youtube.com/@tagtheatre1475/videos', { waitUntil: 'networkidle2' });
  
  // 自動捲動，確保載入更多影片
  await autoScroll(page);

  // 從頁面中抓取影片資訊
  const videos = await page.evaluate(() => {
    const videoElements = document.querySelectorAll('ytd-grid-video-renderer');
    const videoData = [];
    
    videoElements.forEach(video => {
      const titleElem = video.querySelector('#video-title');
      const durationElem = video.querySelector('span.ytd-thumbnail-overlay-time-status-renderer');
      if (titleElem && durationElem) {
        const title = titleElem.textContent.trim();
        const href = titleElem.getAttribute('href');
        const url = href ? 'https://www.youtube.com' + href : '';
        const durationText = durationElem.textContent.trim();  // 格式可能為 "20:15" 或 "1:02:30"
        
        // 轉換影片長度為秒數
        let durationSeconds = 0;
        const parts = durationText.split(':').map(Number);
        if (parts.length === 2) {
          durationSeconds = parts[0] * 60 + parts[1];
        } else if (parts.length === 3) {
          durationSeconds = parts[0] * 3600 + parts[1] * 60 + parts[2];
        }
        
        // 保留播放長度大於或等於 20 分鐘（1200 秒）的影片
        if (durationSeconds >= 20 * 60) {
          videoData.push({ title, url });
        }
      }
    });
    return videoData;
  });

  // 將結果以 "影片標題,影片網址" 的格式寫入文字檔
  const output = videos.map(video => `${video.title},${video.url}`).join('\n');
  fs.writeFileSync('videos.txt', output, 'utf8');
  console.log('已將符合條件的影片網址寫入 videos.txt');

  await browser.close();

  // 自動捲動函式，確保頁面上的更多影片能夠載入
  async function autoScroll(page) {
    await page.evaluate(async () => {
      await new Promise((resolve) => {
        let totalHeight = 0;
        const distance = 100;
        const timer = setInterval(() => {
          const scrollHeight = document.body.scrollHeight;
          window.scrollBy(0, distance);
          totalHeight += distance;
          if (totalHeight >= scrollHeight) {
            clearInterval(timer);
            resolve();
          }
        }, 200);
      });
    });
  }
})();
