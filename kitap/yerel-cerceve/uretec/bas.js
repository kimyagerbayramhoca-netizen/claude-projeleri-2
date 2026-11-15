// Çerçeve sayfalarını basar: HTML → onizleme/<sınıf>-<no>-<ad>.png (deviceScaleFactor 2) [+ PDF] + taşma denetimi.
//   node uretec/bas.js sayfalar/kitap-10.html                 → bütün sayfaların PNG'si
//   node uretec/bas.js sayfalar/kitap-10.html harita zaman     → yalnız adı bu parçaları içeren sayfalar
//   node uretec/bas.js sayfalar/kitap-10.html --pdf cikti.pdf  → ayrıca PDF
// Denetim (yerel-ortak/render.js ile aynı mantık): içerik alanı dışına çıkan öğe ve kutusuna sığmayan metin.
//   Kapaklar ve [data-serbest] öğeler alan denetiminden muaftır.
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

(async () => {
  const arg = process.argv.slice(2);
  const html = path.resolve(arg[0]);
  const pdfIdx = arg.indexOf('--pdf');
  const pdf = pdfIdx >= 0 ? path.resolve(arg[pdfIdx + 1]) : null;
  const sec = arg.slice(1).filter((a, i) => !a.startsWith('--') && (pdfIdx < 0 || i + 1 !== pdfIdx + 1));
  const oniz = path.join(path.dirname(path.dirname(html)), 'onizleme');
  fs.mkdirSync(oniz, { recursive: true });
  const tarayici = await chromium.launch();
  const sayfa = await tarayici.newPage({ viewport: { width: 900, height: 1200 }, deviceScaleFactor: 2 });
  await sayfa.goto('file://' + html, { waitUntil: 'load' });
  await sayfa.evaluate(() => document.fonts.ready);

  const sorunlar = await sayfa.evaluate(() => {
    const mm = v => v * 96 / 25.4;
    const out = [];
    document.querySelectorAll('.sayfa').forEach(s => {
      const ad = s.dataset.ad || '?';
      if (s.classList.contains('kapak-sayfa')) return;
      const sr = s.getBoundingClientRect();
      const ust = sr.top + mm(12), alt = sr.top + mm(283), sol = sr.left + mm(10), sag = sr.right - mm(10);
      s.querySelectorAll('*').forEach(el => {
        if (el.closest('.hud') || el.closest('.alt') || el.closest('svg') || el.closest('[data-serbest]') || el.closest('.ebru-alt')) return;
        const r = el.getBoundingClientRect();
        if (!r.width || !r.height) return;
        const sinif = (el.className && el.className.baseVal === undefined ? el.className : el.tagName) || el.tagName;
        const metin = (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40);
        if (r.bottom > alt + 1 || r.top < ust - 1 || r.left < sol - 1 || r.right > sag + 1)
          out.push(`${ad}: alan dışı [${sinif}] "${metin}" alt=${((r.bottom - sr.top) * 25.4 / 96).toFixed(1)}mm sağ=${((r.right - sr.left) * 25.4 / 96).toFixed(1)}mm`);
        const cs = getComputedStyle(el);
        if (cs.overflow !== 'visible' || el.matches('.kart,.ic-yol,.rota-et,.zs-kart,.madde,.album-yol,.sayfa-turu,.akis-adim,.isaret,.unvan,.sozluk-sutun,.bento'))
          if (el.scrollHeight > el.clientHeight + 2 || (el.scrollWidth > el.clientWidth + 2 && !el.hasAttribute('data-tasma-yatay')))
            out.push(`${ad}: kutu taşması [${sinif}] "${metin}" (${el.scrollWidth}x${el.scrollHeight} > ${el.clientWidth}x${el.clientHeight})`);
      });
      s.querySelectorAll('.rota-et,.basla-et').forEach(el => {
        const r = el.getBoundingClientRect();
        if (r.left < sr.left + mm(2) || r.right > sr.right - mm(2)) out.push(`${ad}: kenara taşan etiket "${el.textContent.trim().slice(0, 30)}"`);
      });
    });
    return out;
  });
  console.log(sorunlar.length ? sorunlar.join('\n') : 'Taşma yok.');

  const bolumler = await sayfa.$$('.sayfa');
  let n = 0;
  for (const b of bolumler) {
    const ad = await b.getAttribute('data-ad');
    if (sec.length && !sec.some(s => ad.includes(s))) continue;
    await b.screenshot({ path: path.join(oniz, `${ad}.png`) });
    n++;
  }
  console.log(`${n} önizleme → ${path.relative(process.cwd(), oniz)}/`);
  if (pdf) {
    await sayfa.pdf({ path: pdf, preferCSSPageSize: true, printBackground: true });
    console.log(`PDF → ${path.relative(process.cwd(), pdf)} (${(fs.statSync(pdf).size / 1048576).toFixed(2)} MB)`);
  }
  await tarayici.close();
})();
