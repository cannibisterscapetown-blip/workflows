const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--force-color-profile=srgb'] });
  const page = await browser.newPage({ viewport: { width: 2600, height: 3700 } });
  await page.goto('file://' + __dirname + '/posters.html', { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(500);
  for (const id of ['pool', 'arcade']) {
    const el = await page.$('#' + id);
    await el.screenshot({ path: `${__dirname}/${id === 'pool' ? 'pool_table_rules' : 'arcade_rules'}.png` });
    console.log('rendered', id);
  }
  await browser.close();
})();
