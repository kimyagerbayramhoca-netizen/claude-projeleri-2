// Genel amaçlı HTML → PNG (tam sayfa) betiği. katalog.py kullanır.
//   node yerel-ortak/fotograf.js girdi.html cikti.png [genislik_px=1400] [olcek=1]
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const [, , girdi, cikti, gen = '1400', olcek = '1'] = process.argv;
  if (!girdi || !cikti) { console.error('kullanım: node fotograf.js girdi.html cikti.png [genislik] [olcek]'); process.exit(1); }
  const tarayici = await chromium.launch();
  const sayfa = await tarayici.newPage({ viewport: { width: +gen, height: 900 }, deviceScaleFactor: +olcek });
  await sayfa.goto('file://' + path.resolve(girdi), { waitUntil: 'load' });
  await sayfa.evaluate(() => document.fonts.ready);
  await sayfa.screenshot({ path: path.resolve(cikti), fullPage: true });
  await tarayici.close();
})();
