// Ünite render betiği: unite.html → PDF + onizleme/sNN.png (deviceScaleFactor 2) + taşma denetimi
// Çalıştır (ünite klasöründen ya da herhangi bir yerden):
//   node yerel-ortak/render.js <ünite-klasörü>            → PDF + bütün PNG'ler
//   node yerel-ortak/render.js <ünite-klasörü> 3 4        → yalnızca 3. ve 4. sayfanın PNG'si (PDF yine üretilir)
//   node yerel-ortak/render.js <ünite-klasörü> --pdfsiz 3 → yalnızca PNG (hızlı deneme)
//   node yerel-ortak/render.js <dosya.html> --pngsiz      → başka yere kurulmuş HTML'den yalnız PDF (dosya.pdf, aynı klasör)
//   Ünite klasörü verilmezse içinde bulunulan klasör kullanılır.
// Denetim iki tür sorunu listeler (yatayda bilerek taşan dekorlu kapsayıcılar data-tasma-yatay ile işaretlenir):
//   • alan dışı   : HUD+çini şeridi altı (12 mm) ile altbilgi üstü (283 mm) arasındaki alandan taşan öğe
//                   (sahne bantları, panorama gibi [data-serbest] öğeler hariç)
//   • kutu taşması: kart, balon, şık gibi kutulara sığmayan metin
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const _arg = process.argv.slice(2);
// hedef: ünite klasörü ya da doğrudan bir .html dosyası (ör. YEREL_CIKTI ile başka yere kurulmuş ünite)
const _hedef = _arg.find(a => !a.startsWith('--') && fs.existsSync(a) && (fs.statSync(a).isDirectory() || a.endsWith('.html')));
const _dosya = _hedef && fs.statSync(_hedef).isFile();
const UNITE = _dosya ? path.dirname(path.resolve(_hedef)) : path.resolve(_hedef || process.cwd());
const HTML = _dosya ? path.resolve(_hedef) : path.join(UNITE, 'unite.html');
const _ad = path.basename(HTML, '.html');
const PDF = path.join(UNITE, (_ad === 'unite' ? path.basename(UNITE) : _ad) + '.pdf');
const ONIZ = path.join(UNITE, _ad === 'unite' ? 'onizleme' : 'onizleme-' + _ad);

(async () => {
  const argv = process.argv.slice(2).filter(a => a !== _hedef);
  const pdfsiz = argv.includes('--pdfsiz');
  const pngsiz = argv.includes('--pngsiz');
  const sec = argv.filter(a => !a.startsWith('--')).map(Number);
  if (!pngsiz) fs.mkdirSync(ONIZ, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 900, height: 1200 }, deviceScaleFactor: 2 });
  await page.goto('file://' + HTML, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);

  const sorunlar = await page.evaluate(() => {
    const mm = v => v * 96 / 25.4;
    const out = [];
    document.querySelectorAll('.sayfa').forEach((s, i) => {
      const sr = s.getBoundingClientRect();
      const ust = sr.top + mm(12), alt = sr.top + mm(283), sol = sr.left + mm(10), sag = sr.right - mm(10);
      s.querySelectorAll('*').forEach(el => {
        if (el.closest('.hud') || el.closest('.alt') || el.closest('svg') || el.closest('[data-serbest]') || el.closest('.ebru-alt')) return;
        const r = el.getBoundingClientRect();
        if (!r.width || !r.height) return;
        const ad = (el.className && el.className.baseVal === undefined ? el.className : el.tagName) || el.tagName;
        const metin = (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 42);
        if (r.bottom > alt + 1 || r.top < ust - 1 || r.left < sol - 1 || r.right > sag + 1)
          out.push(`s${i + 1}: alan dışı [${ad}] "${metin}" alt=${((r.bottom - sr.top) * 25.4 / 96).toFixed(1)}mm`);
        const cs = getComputedStyle(el);
        if (cs.overflow !== 'visible' || el.matches('.kart,.tuzak,.ozet-kart,.balon,.sik,.oy > div,.hazine,.levha,.durak-et,.basamak,.meclis,.kissa,.mesveret,.medeniyet,.esnek,.bento,.mesveret-izgara,.ozetler,.unvanlar,.sandik-izgara,.cozumler'))
          if (el.scrollHeight > el.clientHeight + 2 || (el.scrollWidth > el.clientWidth + 2 && !el.hasAttribute('data-tasma-yatay')))
            out.push(`s${i + 1}: kutu taşması [${ad}] "${metin}" (${el.scrollWidth}x${el.scrollHeight} > ${el.clientWidth}x${el.clientHeight})`);
      });
      // levha ve etiketler sayfa dışına taşmasın
      s.querySelectorAll('.levha,.durak-et').forEach(el => {
        const r = el.getBoundingClientRect();
        if (r.left < sr.left + mm(3) || r.right > sr.right - mm(3)) out.push(`s${i + 1}: kenara taşan etiket "${el.textContent.trim().slice(0, 30)}"`);
      });
    });
    return out;
  });
  console.log(sorunlar.length ? sorunlar.join('\n') : 'Taşma yok.');

  const sayfalar = await page.$$('.sayfa');
  for (let i = 0; i < sayfalar.length && !pngsiz; i++) {
    if (sec.length && !sec.includes(i + 1)) continue;
    await sayfalar[i].screenshot({ path: path.join(ONIZ, `s${String(i + 1).padStart(2, '0')}.png`) });
  }
  if (!pdfsiz) {
    await page.pdf({ path: PDF, preferCSSPageSize: true, printBackground: true });
    const mb = (fs.statSync(PDF).size / 1048576).toFixed(2);
    console.log(`${sayfalar.length} sayfa → ${path.relative(process.cwd(), PDF)} (${mb} MB)`);
  }
  await browser.close();
})();
