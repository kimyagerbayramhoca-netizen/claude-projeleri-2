// HTML -> A4 PDF (Chromium). Kullanım: node pdf.js girdi.html cikti.pdf [onizleme-klasoru]
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const [girdi, cikti, onizleme] = process.argv.slice(2);
  const tarayici = await chromium.launch();
  const sayfa = await tarayici.newPage({ viewport: { width: 794, height: 1123 } });
  await sayfa.goto('file://' + path.resolve(girdi), { waitUntil: 'load' });
  await sayfa.evaluate(() => document.fonts.ready);

  // Taşma denetimi: içerik sayfanın alt sınırını aşıyorsa uyar
  const tasmalar = await sayfa.evaluate(() => {
    const sonuc = [];
    document.querySelectorAll('.sayfa:not(.kapak)').forEach((s, i) => {
      const alt = s.getBoundingClientRect().bottom - 52; // ~14 mm alt boşluk
      s.querySelectorAll(':scope > *:not(.alt-bilgi):not(.ust-serit):not(.arka)').forEach(el => {
        const b = el.getBoundingClientRect().bottom;
        if (b > alt) sonuc.push(`Sayfa ${i + 1}: ${Math.round(b - alt)}px taşma (${el.className || el.tagName})`);
      });
    });
    return sonuc;
  });
  tasmalar.forEach(t => console.warn('UYARI', t));

  if (onizleme) {
    const n = await sayfa.locator('.sayfa').count();
    for (let i = 0; i < n; i++) {
      await sayfa.locator('.sayfa').nth(i).screenshot({ path: path.join(onizleme, `s${String(i + 1).padStart(2, '0')}.png`) });
    }
  }
  await sayfa.emulateMedia({ media: 'print' });
  await sayfa.pdf({ path: cikti, preferCSSPageSize: true, printBackground: true });
  await tarayici.close();
})();
