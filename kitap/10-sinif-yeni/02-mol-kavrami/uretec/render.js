// Ünite render betiği: unite.html → PDF + onizleme/sNN.png (deviceScaleFactor 2)
// Çalıştır (ünite klasöründen ya da herhangi bir yerden):
//   node uretec/render.js            → PDF + tüm PNG'ler
//   node uretec/render.js 3 4        → yalnızca 3. ve 4. sayfanın PNG'si (PDF yine üretilir)
// Ayrıca taşma denetimi yapar: içerik alanının (HUD altı / altbilgi üstü) dışına
// çıkan ya da kutusundan taşan öğeleri listeler.
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const UNITE = path.resolve(__dirname, '..');
const HTML = path.join(UNITE, 'unite.html');
const PDF = path.join(UNITE, path.basename(UNITE) + '.pdf');
const ONIZ = path.join(UNITE, 'onizleme');

(async () => {
  const sec = process.argv.slice(2).map(Number);
  fs.mkdirSync(ONIZ, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 900, height: 1200 }, deviceScaleFactor: 2 });
  await page.goto('file://' + HTML, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);

  // --- taşma denetimi
  const sorunlar = await page.evaluate(() => {
    const mm = v => v * 96 / 25.4;
    const out = [];
    document.querySelectorAll('.sayfa').forEach((s, i) => {
      const sr = s.getBoundingClientRect();
      const ust = sr.top + mm(9.4), alt = sr.top + mm(284), sol = sr.left + mm(11), sag = sr.right - mm(11);
      s.querySelectorAll('*').forEach(el => {
        if (el.closest('.hud') || el.closest('.alt') || el.closest('svg') || el.closest('[data-serbest]')) return;
        const r = el.getBoundingClientRect();
        if (!r.width || !r.height) return;
        const ad = (el.className && el.className.baseVal === undefined ? el.className : el.tagName) || el.tagName;
        const metin = (el.textContent || '').trim().slice(0, 40);
        if (r.bottom > alt + 1 || r.top < ust - 1 || r.left < sol - 1 || r.right > sag + 1)
          out.push(`s${i + 1}: alan dışı [${ad}] "${metin}" alt=${((r.bottom - sr.top) * 25.4 / 96).toFixed(1)}mm`);
        const cs = getComputedStyle(el);
        if (cs.overflow !== 'visible' || el.matches('.kart,.tuzak,.ozet-kart,.balon,.sik,.oy span,.yetenek')) {
          if (el.scrollHeight > el.clientHeight + 2 || el.scrollWidth > el.clientWidth + 2)
            out.push(`s${i + 1}: kutu taşması [${ad}] "${metin}" (${el.scrollWidth}x${el.scrollHeight} > ${el.clientWidth}x${el.clientHeight})`);
        }
      });
    });
    return out;
  });
  console.log(sorunlar.length ? sorunlar.join('\n') : 'Taşma yok.');

  // --- PNG önizlemeler
  const sayfalar = await page.$$('.sayfa');
  for (let i = 0; i < sayfalar.length; i++) {
    if (sec.length && !sec.includes(i + 1)) continue;
    await sayfalar[i].screenshot({ path: path.join(ONIZ, `s${String(i + 1).padStart(2, '0')}.png`) });
  }
  // --- PDF
  await page.pdf({ path: PDF, preferCSSPageSize: true, printBackground: true });
  console.log(`${sayfalar.length} sayfa → ${path.relative(process.cwd(), PDF)}`);
  await browser.close();
})();
