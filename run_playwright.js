const { chromium } = require("playwright");
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  page.on('console', msg => console.log('PAGE LOG:', msg.type(), msg.text()));
  page.on('pageerror', err => console.log('PAGE ERROR:', err));
  await page.goto('http://127.0.0.1:5000', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  const htmlLength = await page.$eval('#app', el => el.innerHTML.length);
  console.log('APP HTML LENGTH', htmlLength);
  await page.screenshot({ path: 'f:/code/python/xingyu/tmp_index_build.png', fullPage: true });
  await browser.close();
})();
