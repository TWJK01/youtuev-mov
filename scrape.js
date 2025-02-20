const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({
    headless: "new",
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  await page.setDefaultNavigationTimeout(0);
  
  // 使用 DOMContentLoaded 快速載入頁面
  await page.goto('https://www.youtube.com/@tagtheatre1475/videos', { waitUntil: 'domcontentloaded' });
  
  // 等待影片列表元素出現
  await page.waitForSelector('ytd-grid-video-renderer', { timeout: 90000 });
  
  // 自動捲動直到不再有新內容出現
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
        const durationText = durationElem.textContent.trim(); // 可能格式 "20:15" 或 "1:02:30"
        
        // 將時間轉成秒數
        let durationSeconds = 0;
        const parts = durationText.split(':').map(Number);
        if (parts.length === 2) {
          durationSeconds = parts[0] * 60 + parts[1];
        } else if (parts.length === 3) {
          durationSeconds = parts[0] * 3600 + parts[1] * 60 + parts[2];
        }
        
        // 只保留大於或等於 20 分鐘（1200 秒）的影片
        if (durationSeconds >= 20 * 60) {
          videoData.push({ title, url });
        }
      }
    });
    return videoData;
  });

  // 將結果寫入文字檔，每行格式：影片標題,影片網址
  const output = videos.map(video => `${video.title},${video.url}`).join('\n');
  fs.writeFileSync('videos.txt', output, 'utf8');
  console.log('已將符合條件的影片網址寫入 videos.txt');
  
  await browser.close();

  // 改進後的自動捲動函式：如果連續 5 次滾動後頁面高度無變化，則認為已到底部
  async function autoScroll(page) {
    await page.evaluate(async () => {
      await new Promise((resolve) => {
        let lastScrollHeight = document.documentElement.scrollHeight;
        let unchangedCount = 0;
        const distance = 100;
        const timer = setInterval(() => {
          window.scrollBy(0, distance);
          const newScrollHeight = document.documentElement.scrollHeight;
          if (newScrollHeight === lastScrollHeight) {
            unchangedCount++;
          } else {
            unchangedCount = 0;
            lastScrollHeight = newScrollHeight;
          }
          // 如果連續 5 次滾動高度沒有變化，則停止滾動
          if (unchangedCount >= 5) {
            clearInterval(timer);
            resolve();
          }
        }, 200);
      });
    });
  }
})();
